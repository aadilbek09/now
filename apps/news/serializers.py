from rest_framework import serializers

from .models import Post


class PostListSerializer(serializers.ModelSerializer):
    """Ro'yxat va 'so'nggi yangiliklar' uchun qisqartirilgan serializer."""

    class Meta:
        model = Post
        fields = ('id', 'title', 'desc', 'category', 'image', 'created_at')


class PostDetailSerializer(serializers.ModelSerializer):
    """Bitta yangilikning to'liq matni uchun serializer."""

    class Meta:
        model = Post
        fields = ('id', 'title', 'desc', 'category', 'content', 'image', 'created_at', 'updated_at')


class PostAdminSerializer(serializers.ModelSerializer):
    """Admin uchun post qo'shish/tahrirlash serializeri."""

    class Meta:
        model = Post
        fields = ('id', 'title', 'desc', 'category', 'content', 'image', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')