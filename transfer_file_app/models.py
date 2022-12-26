import os
import uuid
from django.db import models
from django.dispatch import receiver


class FileUpload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file_name = models.TextField(blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    file = models.FileField()
    uploaded_by = models.ForeignKey(
        'auth.User', related_name='file_uploads', on_delete=models.PROTECT
    )

    def save(self, *args, **kwargs):
        if self.file:
            self.file_name = self.file.name
            self.file_size = self.file.size
            file_name, file_extension = os.path.splitext(self.file_name)
            self.file.name = '{}_{}{}'.format(
                file_name, uuid.uuid4().hex, file_extension)

        super(FileUpload, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=FileUpload)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
