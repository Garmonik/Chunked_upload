# Generated by Django 4.1 on 2022-08-31 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drf_chunked_upload', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChunkedUpload',
        ),
    ]