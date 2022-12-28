import base64
import json
from datetime import datetime

from Crypto.Cipher import AES
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from file_management_app.models import File


class DownloadFileView(APIView):

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request):
        ciphertext = self.request.query_params.get('ciphertext')
        tag = self.request.query_params.get('tag')
        nonce = self.request.query_params.get('nonce')

        ciphertext = base64.b64decode(ciphertext)
        tag = base64.b64decode(tag)
        nonce = base64.b64decode(nonce)

        cipher = AES.new(bytes(settings.AES_KEY, 'ascii'), AES.MODE_EAX, nonce)
        payload = cipher.decrypt_and_verify(ciphertext, tag)
        payload = json.loads(payload)

        due_date = datetime.fromisoformat(payload.get('due_date'))
        if due_date < datetime.now():
            return Response(status=status.HTTP_403_FORBIDDEN)

        file = self.get_object(payload.get('file_id'))
        file_response = FileResponse(
            file.file.open(), as_attachment=True, filename=file.file_name
        )
        file_response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return file_response
