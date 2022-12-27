from django.db import transaction
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from file_management_app.models import File
from file_management_app.serializers import FileSerializer


class UploadFileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    @transaction.atomic
    def post(self, request):
        files = request.FILES

        for key in files:
            file = files.get(key)
            file_serializer = FileSerializer(data={
                'file': file,
            })
            if not file_serializer.is_valid():
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            file_serializer.save(owner=self.request.user)

        return Response(status=status.HTTP_201_CREATED)
