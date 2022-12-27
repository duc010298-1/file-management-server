from django.urls import path, include

urlpatterns = [
    path('file/', include('file_management_app.module.file.urls')),
]
