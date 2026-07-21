from rest_framework import serializers

from .models import Message, NewsletterSubscriber, Testimonial


class MessageCreateSerializer(serializers.ModelSerializer):
    """POST /api/contact — Sayt kontakt formasi orqali xabar yuborish."""

    class Meta:
        model = Message
        fields = ('id', 'name', 'email', 'phone', 'subject', 'text', 'created_at')
        read_only_fields = ('id', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    """GET /api/admin/messages — Admin uchun barcha xabarlar."""

    class Meta:
        model = Message
        fields = ('id', 'name', 'email', 'phone', 'subject', 'text', 'reply', 'reply_created_at', 'is_read', 'created_at')
        read_only_fields = fields


class MessageReplySerializer(serializers.Serializer):
    """PATCH /api/admin/messages/{id}/reply — Admin javob yozish."""

    reply = serializers.CharField()


class NewsletterSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ('id', 'email', 'subscribed_at')
        read_only_fields = ('id', 'subscribed_at')


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ('id', 'name', 'text', 'image', 'rating', 'created_at')
        read_only_fields = ('id', 'created_at')
