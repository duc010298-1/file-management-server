from django.db import transaction
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from file_management_app.models import File


class DeleteFileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    @transaction.atomic
    def delete(self, request, pk):
        file = self.get_object(pk)
        if file.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
