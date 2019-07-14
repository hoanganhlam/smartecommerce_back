from rest_framework import serializers
from media import models
from sorl.thumbnail import get_thumbnail


class MediaSerializer(serializers.ModelSerializer):
    thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = models.Media
        fields = ['id', 'title', 'description', 'user', 'thumbnails', 'file', 'created']
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def get_thumbnails(self, obj):
        return {
            'thumb_100_100': get_thumbnail(obj.file, '100x100', crop='100% center', quality=100).url,
            'thumb_200_123': get_thumbnail(obj.file, '200x123', crop='100% center', quality=100).url,
            'thumb_150_150': get_thumbnail(obj.file, '150x150', crop='100% center', quality=100).url,
            'thumb_200_250': get_thumbnail(obj.file, '200x250', crop='100% center', quality=100).url,
        }
