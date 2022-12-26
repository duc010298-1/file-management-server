from django.db import transaction
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from transfer_file_app.models import FileUpload


class DeleteFileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return FileUpload.objects.get(pk=pk)
        except FileUpload.DoesNotExist:
            raise Http404

    @transaction.atomic
    def delete(self, request, pk):
        file_upload = self.get_object(pk)
        file_upload.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
