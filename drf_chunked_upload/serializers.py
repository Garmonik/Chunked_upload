from rest_framework import serializers
from rest_framework.reverse import reverse
import subprocess as sp
import shlex
import json

from drf_chunked_upload.models import ChunkedUpload, video_extension, image_extension, gif_extension


class ChunkedUploadSerializer(serializers.ModelSerializer):
    viewname = 'chunkedupload-detail'
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse(self.viewname,
                       kwargs={'pk': obj.id},
                       request=self.context['request'])

    class Meta:
        model = ChunkedUpload
        fields = '__all__'
        read_only_fields = ('status', 'completed_at')


class UploadFileSerializer(serializers.ModelSerializer):
    viewname = 'chunkedupload-detail'
    url = serializers.SerializerMethodField()
    type_media = serializers.SerializerMethodField()
    codec_name = serializers.SerializerMethodField()
    type_extension = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()

    def get_width(self, obj):
        file = '.' + obj.file.url
        data = sp.run(shlex.split(f'ffprobe -loglevel error -show_streams -of json {file}'), capture_output=True).stdout
        d = json.loads(data)
        obj.width = d['streams'][0]['width']
        obj.save()
        return obj.width

    def get_height(self, obj):
        file = '.' + obj.file.url
        data = sp.run(shlex.split(f'ffprobe -loglevel error -show_streams -of json {file}'), capture_output=True).stdout
        d = json.loads(data)
        obj.height = d['streams'][0]['height']
        obj.save()
        return obj.height

    def get_type_extension(self, obj):
        obj.file_extension = obj.filename.split('.')[-1]
        return obj.file_extension

    def get_codec_name(self, obj):
        file = '.' + obj.file.url
        data = sp.run(shlex.split(f'ffprobe -loglevel error -show_streams -of json {file}'), capture_output=True).stdout
        d = json.loads(data)
        obj.codec_name = d['streams'][0]['codec_name']
        obj.save()
        return obj.codec_name

    def get_type_media(self, obj):
        if obj.filename.split('.')[-1] in video_extension:
            obj.type_media = 'video'
            obj.save()
            return 'video'
        if obj.filename.split('.')[-1] in image_extension:
            obj.type_media = 'image'
            obj.save()
            return 'image'
        if obj.filename.split('.')[-1] in gif_extension:
            obj.type_media = 'gif'
            obj.save()
            return 'gif'

    def get_url(self, obj):
        return reverse(self.viewname,
                       kwargs={'pk': obj.id},
                       request=self.context['request'])

    class Meta:
        model = ChunkedUpload
        fields = '__all__'
        read_only_fields = ('status', 'completed_at')
