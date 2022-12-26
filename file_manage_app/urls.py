from django.urls import path, include

urlpatterns = [
    path('file/', include('file_manage_app.module.file_upload.urls')),
]
