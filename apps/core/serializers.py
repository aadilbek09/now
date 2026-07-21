from rest_framework import serializers

from .models import GalleryImage, RestaurantInfo


class ImageUploadSerializer(serializers.Serializer):
    """POST /api/upload/image — Uluwma foto ju'klew ushin serializer."""

    image = serializers.ImageField()


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ('id', 'image', 'caption', 'created_at')
        read_only_fields = ('id', 'created_at')


class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInfo
        fields = (
            'id', 'address', 'phone', 'working_hours',
            'map_url', 'instagram_url', 'facebook_url', 'updated_at',
        )
        read_only_fields = ('id', 'updated_at')
