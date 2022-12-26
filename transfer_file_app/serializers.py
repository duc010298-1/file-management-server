from rest_framework import serializers

from transfer_file_app.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'
