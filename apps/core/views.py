import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse, Http404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole
from .models import GalleryImage, RestaurantInfo
from .serializers import (
    GalleryImageSerializer,
    ImageUploadSerializer,
    RestaurantInfoSerializer,
)


class ImageUploadView(APIView):
    """
    POST /api/upload/image — Ba'rshe fotoni ju'klew endpointi.
    Ba'rshe modullar (menu, news, contact/testimonials) usidan paydalanadi:
    fayl 'uploads/' papkasina saqlanadi ha'm onin' URL manzili qaytariladi;
    qaytqan URL basqa modeldin' `image` maydanina (misali Product.image)
    jazip qoyiladi. Bul jerde uluma "Gallery" jadvaliga jazilmaydi —
    Gallery tek qana Instagram-fotolar ushin bo'lek islenedi.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_file = serializer.validated_data['image']

        ext = image_file.name.rsplit('.', 1)[-1] if '.' in image_file.name else 'jpg'
        filename = f"uploads/{uuid.uuid4().hex}.{ext}"
        saved_path = default_storage.save(filename, image_file)
        image_url = request.build_absolute_uri(default_storage.url(saved_path))

        return Response(
            {'path': saved_path, 'url': image_url},
            status=status.HTTP_201_CREATED,
        )


class GalleryListView(generics.ListAPIView):
    """GET /api/gallery — Instagram Gallery fotolari."""

    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class RestaurantInfoView(APIView):
    """GET /api/restaurant-info — Ma'nzil, telefon, jumis waqti, karta."""

    permission_classes = [AllowAny]

    def get(self, request):
        info = RestaurantInfo.objects.first()
        if not info:
            return Response(
                {'detail': "Restoran mag'liwmatlari ele kiritilmegen!."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(RestaurantInfoSerializer(info).data)


class AdminGalleryCreateView(generics.CreateAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]


class AdminGalleryDeleteView(generics.DestroyAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [IsAdminRole]


class AdminRestaurantInfoUpdateView(generics.UpdateAPIView):
    queryset = RestaurantInfo.objects.all()
    serializer_class = RestaurantInfoSerializer
    permission_classes = [IsAdminRole]


# ---------- Frontend (Static HTML) ----------
FRONTEND_DIR = os.path.join(settings.BASE_DIR, 'static', 'frontend')


def serve_frontend(request, page='index.html'):
    """
    Frontend HTML fayllarini xizmat qilish (Django orqali).
    / -> static/frontend/index.html
    /menu/ -> static/frontend/menu.html
    """
    if not page.endswith('.html'):
        page += '.html'
    file_path = os.path.join(FRONTEND_DIR, page)
    if not os.path.exists(file_path):
        raise Http404('Sahifa topilmadi')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content)
