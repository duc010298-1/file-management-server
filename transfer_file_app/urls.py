from django.urls import path, include

urlpatterns = [
    path('file/', include('transfer_file_app.module.file_upload.urls')),
]
