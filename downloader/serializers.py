from rest_framework import serializers


class VideoSerializer(serializers.Serializer):
    youtube_url = serializers.URLField()


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()