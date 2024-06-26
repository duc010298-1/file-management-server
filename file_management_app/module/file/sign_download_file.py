import base64
import json
from datetime import datetime

from Crypto.Cipher import AES
from django.conf import settings
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from file_management_app.models import File
import json


class SignDownloadFileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request):
        list_file_id = json.loads(request.GET.get('list_file_id'))
        for id in list_file_id:
            file = self.get_object(id)
            if file.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

        due_date = datetime.now() + settings.SIGN_URL_LIFE_TIME
        payload = {
            'list_file_id': list_file_id,
            'due_date': due_date.isoformat()
        }
        payload = json.dumps(payload).encode('ascii')

        cipher = AES.new(bytes(settings.AES_KEY, 'ascii'), AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(payload)
        nonce = cipher.nonce

        ciphertext = base64.b64encode(ciphertext)
        tag = base64.b64encode(tag)
        nonce = base64.b64encode(nonce)

        return Response({
            'ciphertext': ciphertext,
            'tag': tag,
            'nonce': nonce,
        })
