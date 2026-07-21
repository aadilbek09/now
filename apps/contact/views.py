from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole
from .models import Message, NewsletterSubscriber, Testimonial
from .serializers import (
    MessageCreateSerializer,
    MessageSerializer,
    NewsletterSubscribeSerializer,
    TestimonialSerializer,
)

MSG_TAG = ["5. Xabarlar & Kontakt"]
NEWSLETTER_TAG = ["5. Newsletter"]
TESTIMONIAL_TAG = ["5. Testimonials"]


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=MSG_TAG, operation_summary="Kontakt formasi orqali xabar yuborish",
    ),
)
class ContactMessageCreateView(generics.CreateAPIView):
    """POST /api/contact — Sayt kontakt formasi orqali xabar yuborish."""

    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    permission_classes = [AllowAny]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=MSG_TAG, operation_summary="Barcha xabarlar (Admin)"),
)
class AdminMessageListView(generics.ListAPIView):
    """GET /api/admin/messages — Admin uchun barcha xabarlar."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAdminRole]


@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(tags=MSG_TAG, operation_summary="Xabarni o'qilgan deb belgilash (Admin)"),
)
class AdminMessageMarkReadView(APIView):
    """PATCH /api/admin/messages/{id}/read — Xabarni o'qilgan deb belgilash."""

    permission_classes = [IsAdminRole]

    def patch(self, request, id):
        try:
            message = Message.objects.get(id=id)
        except Message.DoesNotExist:
            return Response({'detail': 'Xabar topilmadi.'}, status=404)
        message.is_read = True
        message.save(update_fields=['is_read'])
        return Response(MessageSerializer(message).data)


@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(tags=MSG_TAG, operation_summary="Xabarni o'chirish (Admin)"),
)
class AdminMessageDeleteView(generics.DestroyAPIView):
    """DELETE /api/admin/messages/{id} — Xabarni o'chirish."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAdminRole]
    lookup_url_kwarg = 'id'


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(tags=NEWSLETTER_TAG, operation_summary="Newsletter obunasi"),
)
class NewsletterSubscribeView(generics.CreateAPIView):
    """POST /api/newsletter/subscribe — Newsletter obunasi."""

    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscribeSerializer
    permission_classes = [AllowAny]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=TESTIMONIAL_TAG, operation_summary="Mijozlar sharhlari ro'yxati"),
)
class TestimonialListView(generics.ListAPIView):
    """GET /api/testimonials — Mijozlar sharhlari ro'yxati."""

    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class AdminTestimonialCreateView(generics.CreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminRole]


class AdminTestimonialUpdateView(generics.UpdateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminRole]


class AdminTestimonialDeleteView(generics.DestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminRole]


class AdminNewsletterSubscriberListView(generics.ListAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscribeSerializer
    permission_classes = [IsAdminRole]
