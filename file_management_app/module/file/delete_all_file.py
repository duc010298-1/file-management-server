from django.db import transaction
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from file_management_app.models import File


class DeleteAllFileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def delete(self, request):
        user = request.user
        files = File.objects.filter(owner=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
