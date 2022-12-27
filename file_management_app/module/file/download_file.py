from django.http import FileResponse, Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from file_management_app.models import File


class DownloadFileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = request.user
        file = self.get_object(pk)
        if file.owner != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        file_response = FileResponse(
            file.file.open(), as_attachment=True, filename=file.file_name
        )
        file_response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return file_response
