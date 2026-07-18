from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny

from apps.accounts.permissions import IsAdminRole
from .models import Post
from .serializers import PostAdminSerializer, PostDetailSerializer, PostListSerializer

TAG = ["3. Yangiliklar / Postlar"]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=TAG, operation_summary="Barcha yangiliklar (paginatsiya bilan)"),
)
class PostListView(generics.ListAPIView):
    """GET /api/posts — Barcha yangiliklar (paginatsiya bilan)."""

    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=TAG, operation_summary="So'nggi 3 ta yangilik"),
)
class PostLatestView(generics.ListAPIView):
    """GET /api/posts/latest — So'nggi 3 ta yangilik (bosh sahifa uchun)."""

    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Post.objects.all()[:3]


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(tags=TAG, operation_summary="Bitta yangilik to'liq matni"),
)
class PostDetailView(generics.RetrieveAPIView):
    """GET /api/posts/{id} — Bitta yangilik to'liq matni."""

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'id'


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(tags=TAG, operation_summary="Yangi post qo'shish (Admin)"),
)
class AdminPostCreateView(generics.ListCreateAPIView):
    """GET/POST /api/admin/posts — Postlar ro'yxati va yangi post qo'shish."""

    queryset = Post.objects.all()
    serializer_class = PostAdminSerializer
    permission_classes = [IsAdminRole]


@method_decorator(
    name='put',
    decorator=swagger_auto_schema(tags=TAG, operation_summary="Postni to'liq tahrirlash (Admin)"),
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(tags=TAG, operation_summary="Postni qisman tahrirlash (Admin)"),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(tags=TAG, operation_summary="Postni o'chirish (Admin)"),
)
class AdminPostDetailView(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    """
    /api/admin/posts/{id}
    PUT    — Postni to'liq tahrirlash
    PATCH  — Postni qisman tahrirlash
    DELETE — Postni o'chirish
    """

    queryset = Post.objects.all()
    serializer_class = PostAdminSerializer
    permission_classes = [IsAdminRole]
    lookup_url_kwarg = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)