import os
import json
import re
import PyPDF2
import docx
import rdflib
from pydantic import BaseModel
from typing import List, Optional, Dict
from dotenv import load_dotenv

load_dotenv()

# Define your data models
class ContactInfo(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    linkedin: Optional[str]

class PersonalDetails(BaseModel):
    full_name: str
    contact_info: ContactInfo
    professional_summary: Optional[str]

class Education(BaseModel):
    institution: Optional[str]
    degree: Optional[str]
    field_of_study: Optional[str]
    graduation_date: Optional[str]

class WorkExperience(BaseModel):
    company: Optional[str]
    title: Optional[str]
    duration: Optional[str]
    notable_contributions: Optional[List[str]]

class Resume(BaseModel):
    personal_details: PersonalDetails
    education: List[Education] = []
    work_experience: List[WorkExperience] = []
    skills: List[str] = []
    certifications: List[str] = []
    publications: List[str] = []
    awards: List[str] = []
    additional_sections: Optional[Dict] = None

def pdf_to_string(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
    return text

def docx_to_string(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def doc_to_string(file_path):
    return "DOC format not supported. Please use PDF or DOCX."

def rdf_to_string(file_path):
    graph = rdflib.Graph()
    graph.parse(file_path)
    text = graph.serialize(format='turtle')
    return text.decode('utf-8') if isinstance(text, bytes) else text

def file_to_string(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return pdf_to_string(file_path)
    elif ext == '.docx':
        return docx_to_string(file_path)
    elif ext == '.doc':
        return doc_to_string(file_path)
    elif ext == '.rdf':
        return rdf_to_string(file_path)
    else:
        return None

# def extract_resume_fields(full_text):
#     # Construct a prompt that instructs the API to output valid JSON without markdown
#     prompt = f"""Analyze the resume provided below and output a JSON object with the following keys:
# - "personalDetails": an object with "name", "contactInfo" (with "phone", "email", "url") and "summary".
# - "education": an array of objects (each with "institution", "degree", "fieldOfStudy", "graduationDate").
# - "workExperience": an array of objects (each with "company", "position", "employmentDuration", and "notableContributions").
# Output only valid JSON (no markdown or extra text).

# Resume:
# {full_text}
#     """
#     # Try Google Gemini API first
#     try:
#         from langchain_google_genai import ChatGoogleGenerativeAI
#         gemini = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_GENAI_API_KEY"))
#         result = gemini.generate(prompt)
#         result_data = json.loads(result)
#         print("Google Gemini result:", result_data)
#         return result_data
#     except Exception as e:
#         print("Google Gemini API failed, falling back to Hugging Face. Error:", e)
#         # Fallback: Use Hugging Face API
#         try:
#             from huggingface_hub import InferenceClient
#             client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=os.getenv("HF_TOKEN"))
#             response = client.chat_completion(
#                 messages=[
#                     {"role": "system", "content": "You are an assistant that extracts resume fields."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=1024,
#                 temperature=0.7,
#                 top_p=0.95,
#                 stream=False
#             )
#             full_response = response['choices'][0]['message']['content']
#             # Remove markdown code block markers if present
#             full_response = re.sub(r"^```json\s*", "", full_response)
#             full_response = re.sub(r"\s*```$", "", full_response)
#             print("Hugging Face full response:", full_response)
#             result_data = json.loads(full_response)
#             return result_data
#         except Exception as hf_e:
#             print("Hugging Face API also failed. Error:", hf_e)
#             raise Exception("Both API calls failed.")
import requests
import datetime
def parse_with_new_api(file_path: str) -> Optional[Dict]:
    """Call the new resume parsing API with the file."""
    url = "https://foxsense.keka.com/careers/api/resumeparser/default/2"
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(url, files=files)
            response.raise_for_status()  # Raise HTTP errors
            return response.json()
    except Exception as e:
        print(f"New API call failed: {str(e)}")
        return None

def map_api_response(api_data: Dict) -> Dict:
    """Map the new API response to our existing format."""
    def parse_date(iso_date: str) -> str:
        try:
            return datetime.datetime.fromisoformat(iso_date).strftime("%b %Y")
        except:
            return ""
    
    candidate = api_data.get("candidateProfile", {})
    contact = candidate.get("mobilePhone", {})
    
    # Personal Details
    personal_details = {
        "name": candidate.get("displayName", ""),
        "contactInfo": {
            "email": [candidate.get("email", "")],
            "phone": [f"{contact.get('countryCode', '')}{contact.get('number', '')}"],
            "url": ""
        },
        "summary": ""
    }
    
    # Education
    education = []
    for edu in candidate.get("educationDetails", []):
        education.append({
            "institution": edu.get("university", ""),
            "degree": edu.get("degree", ""),
            "fieldOfStudy": edu.get("branch", ""),
            "graduationDate": ""  # Not available in API response
        })
    
    # Work Experience
    work_experience = []
    for exp in candidate.get("experienceDetails", []):
        start_date = parse_date(exp.get("dateOfJoining", ""))
        end_date = parse_date(exp.get("dateOfRelieving", ""))
        duration = f"{start_date} - {end_date}" if start_date and end_date else "N/A"
        
        work_experience.append({
            "company": exp.get("companyName", ""),
            "position": exp.get("designation", ""),
            "employmentDuration": duration,
            "notableContributions": []
        })
    work_experiences = candidate.get("standardFields", {}).get("workExperience", {})
    exp_answer = work_experiences.get("answer", {})
    experience_data = json.loads(exp_answer) if isinstance(exp_answer, str) else exp_answer

    years = experience_data.get("Years", 0)
    months = experience_data.get("Months", 0)
    total_months = experience_data.get("TotalMonths", 0)

    education_details = candidate.get("educationDetails", [])

    # Get the first degree if available
    first_degree = education_details[0].get("degree", "") if education_details else ""

    # print(f"Years: {years}, Months: {months}, Total Months: {total_months}")
    total_experience = f"{years} years {months} months"
    # Skills
    skills = [s.get("name", "") for s in candidate.get("skills", [])]
    # print(skills)
    return {
        "personalDetails": personal_details,
        "education": education,
        "workExperience": work_experience,
        "totalExperience": total_experience,
        "skills": skills,
        "first_degree": first_degree,
        "certifications": [],
        "publications": [],
        "awards": [],
        "additional_sections": None
    }

def extract_resume_fields(full_text: str, file_path: Optional[str] = None) -> Dict:
    """Main extraction function with fallback logic."""
    # Try new API first if file_path is available
    if file_path:
        try:
            api_response = parse_with_new_api(file_path)
            if api_response:
                print("Using new API response")
                return map_api_response(api_response)
        except Exception as e:
            print(f"New API failed, falling back. Error: {str(e)}")
    
    # Existing Gemini/HuggingFace implementation
    prompt = f"""Analyze the resume provided below and output a JSON object..."""  # Keep original prompt
    
    try:
        # Gemini implementation
        from langchain_google_genai import ChatGoogleGenerativeAI
        gemini = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_GENAI_API_KEY"))
        result = gemini.generate(prompt)
        result_data = json.loads(result)
        return result_data
    except Exception as e:
        print("Google Gemini failed, trying Hugging Face...")
        
        try:
            # HuggingFace implementation
            from huggingface_hub import InferenceClient
            client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=os.getenv("HF_TOKEN"))
            response = client.chat_completion(...)
            # ... keep existing Hugging Face logic ...
            return result_data
        except Exception as hf_e:
            raise Exception("All parsing methods failed")