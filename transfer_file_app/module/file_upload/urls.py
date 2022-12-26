from django.urls import path

from transfer_file_app.module.file_upload.download_file import DownloadFileView
from transfer_file_app.module.file_upload.upload_file import UploadFileView

urlpatterns = [
    path('upload-file/', UploadFileView.as_view()),
    path('download-file/<int:pk>/', DownloadFileView.as_view()),
]
