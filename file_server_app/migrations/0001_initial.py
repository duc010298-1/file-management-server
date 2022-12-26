# Generated by Django 4.1.4 on 2022-12-26 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('file_name', models.TextField(null=True)),
                ('file_size', models.PositiveIntegerField(null=True)),
                ('file', models.FileField(upload_to='')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='file_uploads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]