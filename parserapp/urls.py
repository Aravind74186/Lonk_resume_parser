from django.urls import path
from .views import UploadResumesView, download_excel

urlpatterns = [
    path('', UploadResumesView.as_view(), name='upload_resumes'),
    path('download/', download_excel, name='download_excel'),
]
