from django.db import transaction
from django.http import FileResponse, Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from transfer_file_app.models import FileUpload
from transfer_file_app.serializers import FileUploadSerializer


class DownloadFileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return FileUpload.objects.get(pk=pk)
        except FileUpload.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        file_upload = self.get_object(pk)
        return FileResponse(file_upload.file.open(), as_attachment=True, filename=file_upload.file_name)
