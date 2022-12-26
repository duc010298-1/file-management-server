from django.db import transaction
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from file_server_app.models import FileUpload
from file_server_app.serializers import FileUploadSerializer


class UploadFileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return FileUpload.objects.get(pk=pk)
        except FileUpload.DoesNotExist:
            raise Http404

    @transaction.atomic
    def post(self, request):
        files = request.FILES

        for key in files:
            file = files.get(key)
            file_upload_serializer = FileUploadSerializer(data={
                'file': file,
            })
            if not file_upload_serializer.is_valid():
                return Response(file_upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            file_upload_serializer.save(uploaded_by=self.request.user)

        return Response(status=status.HTTP_201_CREATED)
