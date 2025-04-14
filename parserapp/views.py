import os
import tempfile
import json
from django.shortcuts import render
from django.views import View
from .forms import ResumeUploadForm
from . import resume_helpers

class UploadResumesView(View):
    template_name = 'parserapp/upload.html'

    def get(self, request):
        form = ResumeUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ResumeUploadForm(request.POST, request.FILES)
        parsed_results = []
        if form.is_valid():
            files = request.FILES.getlist('resumes')
            for f in files:
                extension = os.path.splitext(f.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
                    for chunk in f.chunks():
                        tmp_file.write(chunk)
                    tmp_file_path = tmp_file.name

                full_text = resume_helpers.file_to_string(tmp_file_path)
                if full_text:
                    try:
                        # Pass both full_text AND file_path to the updated function
                        result = resume_helpers.extract_resume_fields(full_text, tmp_file_path)
                        # Normalize contactInfo: ensure email and phone are lists.
                        personal = result.get("personalDetails", {})
                        contact = personal.get("contactInfo", {})
                        if isinstance(contact.get("email", ""), str):
                            contact["email"] = [contact.get("email", "")]
                        if isinstance(contact.get("phone", ""), str):
                            contact["phone"] = [contact.get("phone", "")]
                        
                        # Create an "experience" field by summarizing work experience details.
                        work_exps = result.get("workExperience", [])
                        if work_exps:
                            positions = [exp.get("position", "") for exp in work_exps if exp.get("position")]
                            result["experience"] = ", ".join(positions) if positions else "N/A"
                        else:
                            result["experience"] = "N/A"

                        total_exps = result.get("totalExperience", [])
                        first_degree = result.get("first_degree", [])
                        result["first_degree"] = first_degree
                        result["total_exps"] = total_exps
                        
                        
                        parsed_results.append(result)
                    except Exception as e:
                        # Append a default record with an error indicator so that the row appears
                        error_record = {
                            "personalDetails": {
                                "name": f"{f.name} (Parsing Failed)",
                                "contactInfo": {
                                    "email": ["N/A"],
                                    "phone": ["N/A"],
                                    "url": ""
                                },
                                "summary": ""
                            },
                            "education": [],
                            "workExperience": [],
                            "experience": "N/A",
                            "created_date": "Mar 05, 2025 00:19 AM",
                            "last_track_time": "Mar 05, 2025 00:19 AM",
                            "current_city": "N/A",
                            "error": str(e)
                        }

                        parsed_results.append(error_record)
            os.remove(tmp_file_path)

            request.session['parsed_results'] = json.dumps(parsed_results)
            return render(request, 'parserapp/results.html', {'results': parsed_results})
        else:
            print("Form is invalid", form.errors)
        return render(request, self.template_name, {'form': form})

def download_excel(request):
    import pandas as pd
    parsed_json = request.session.get('parsed_results')
    if not parsed_json:
        return render(request, 'parserapp/results.html', {'results': []})
    parsed_results = json.loads(parsed_json)

    # Example: flatten all resumes into multiple rows OR just the first one.
    # Here we assume you only export the first result, but you can loop over all if needed.
    rows = []
    for result in parsed_results:
        personal = result.get('personalDetails', {})
        contact = personal.get('contactInfo', {})
        row = {
            'Name': personal.get('name', ''),
            'Phone': (
                ", ".join(contact.get('phone', [])) 
                if isinstance(contact.get('phone', []), list) 
                else contact.get('phone', '')
            ),
            'Email': (
                ", ".join(contact.get('email', [])) 
                if isinstance(contact.get('email', []), list) 
                else contact.get('email', '')
            ),
            'Summary': personal.get('summary', ''),
            'Experience': result.get('experience', ''),  # or a computed value
            'Created Date': result.get('created_date', ''),
            'Last Track Time': result.get('last_track_time', ''),
            'Current City': result.get('current_city', ''),
            # Add any other fields you want to export, e.g. Skills, Education, etc.
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        df.to_excel(tmp.name, index=False)
        tmp.seek(0)
        excel_data = tmp.read()

    from django.http import HttpResponse
    response = HttpResponse(
        excel_data, 
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="parsed_resumes.xlsx"'
    return response
