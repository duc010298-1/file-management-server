import os
from django.db import models
from django.dispatch import receiver


class FileUpload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
    file_size = models.PositiveIntegerField()
    uploaded_by = models.ForeignKey('auth.User', related_name='file_uploads', on_delete=models.PROTECT)


@receiver(models.signals.post_delete, sender=FileUpload)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
