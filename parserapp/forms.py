from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput

class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def to_python(self, data):
        if not data:
            return []
        if isinstance(data, list):
            return data
        return [data]

    def validate(self, data):
        if not data:
            raise ValidationError("No file was submitted. Check the encoding type on the form.")
        for uploaded_file in data:
            super(MultiFileField, self).validate(uploaded_file)

class ResumeUploadForm(forms.Form):
    resumes = MultiFileField()
