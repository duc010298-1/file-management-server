from django.urls import path, include

urlpatterns = [
    path('file/', include('file_server_app.module.file_upload.urls')),
]
