from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import GeneratedUrls


class GeneratedUrlsSerializer(ModelSerializer):
    origin_url = serializers.URLField(write_only=True)
    generated_url = serializers.CharField(read_only=True)

    class Meta:
        model = GeneratedUrls
        fields = ['origin_url', 'generated_url']
