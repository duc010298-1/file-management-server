from django.urls import path

from file_management_app.module.file.delete_all_file import DeleteAllFileView
from file_management_app.module.file.delete_file import DeleteFileView
from file_management_app.module.file.download_file import DownloadFileView
from file_management_app.module.file.get_list_file import GetListFileView
from file_management_app.module.file.sign_download_file import \
    SignDownloadFileView
from file_management_app.module.file.upload_file import UploadFileView

urlpatterns = [
    path('list-file/', GetListFileView.as_view()),
    path('upload-file/', UploadFileView.as_view()),
    path('download-file/', DownloadFileView.as_view()),
    path('sign-download-file/<int:pk>/', SignDownloadFileView.as_view()),
    path('delete-file/<int:pk>/', DeleteFileView.as_view()),
    path('delete-all-file/', DeleteAllFileView.as_view()),
]
