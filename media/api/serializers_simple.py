from rest_framework import serializers
from media import models


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = ['id', 'title', 'description', 'file', 'created']
