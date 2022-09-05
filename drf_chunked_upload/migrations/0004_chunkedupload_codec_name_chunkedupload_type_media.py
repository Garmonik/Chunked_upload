# Generated by Django 4.1 on 2022-09-05 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drf_chunked_upload', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunkedupload',
            name='codec_name',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='chunkedupload',
            name='type_media',
            field=models.CharField(blank=True, choices=[('image', 'image'), ('video', 'video'), ('gif', 'gif')], max_length=8, null=True),
        ),
    ]