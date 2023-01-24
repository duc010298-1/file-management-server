import base64
import json
import zipfile
from datetime import datetime
from io import BytesIO

from Crypto.Cipher import AES
from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse
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

        list_file_id = payload.get('list_file_id')
        files = []
        for id in list_file_id:
            files.append(self.get_object(id))
        if len(files) == 1:
            file_response = FileResponse(
                files[0].file.open(), as_attachment=True, filename=files[0].file_name
            )
            file_response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return file_response
        else:
            in_memory = BytesIO()
            zip = zipfile.ZipFile(in_memory, 'w', zipfile.ZIP_DEFLATED, False)
            for file in files:
                zip.writestr(file.file_name, file.file.read())
            # fix for Linux zip files read in Windows
            for file in zip.filelist:
                file.create_system = 0
            zip.close()

            zip_file_name = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            response = HttpResponse('', content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=%s.zip' % zip_file_name
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            in_memory.seek(0)
            response.write(in_memory.read())

            return response
