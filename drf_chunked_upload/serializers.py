from rest_framework import serializers
from rest_framework.reverse import reverse

from drf_chunked_upload.models import ChunkedUpload, video_extension, image_extension, gif_extension


class ChunkedUploadSerializer(serializers.ModelSerializer):
    viewname = 'chunkedupload-detail'
    url = serializers.SerializerMethodField()
    type_media = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()

    def get_file_extension(self, obj):
        obj.file_extension = obj.filename.split('.')[-1]
        return obj.file_extension

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
