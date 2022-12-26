from django.urls import path

from file_server_app.module.file_upload.delete_file import DeleteFileView
from file_server_app.module.file_upload.download_file import DownloadFileView
from file_server_app.module.file_upload.get_list_file import GetListFileView
from file_server_app.module.file_upload.upload_file import UploadFileView

urlpatterns = [
    path('list-file/', GetListFileView.as_view()),
    path('upload-file/', UploadFileView.as_view()),
    path('download-file/<int:pk>/', DownloadFileView.as_view()),
    path('delete-file/<int:pk>/', DeleteFileView.as_view()),
]
