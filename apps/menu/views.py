from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole

from .models import (
    Category,
    Product,
    ProductComment,
    ProductLike,
    ProductRating,
)
from .serializers import (
    AdminProductSerializer,
    CategorySerializer,
    ProductCommentCreateSerializer,
    ProductCommentSerializer,
    ProductLikeSerializer,
    ProductRatingSerializer,
    ProductSerializer,
    ProductToggleSerializer,
)


# ---------- Public ----------

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class PopularProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True, is_popular=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


# ---------- Admin: Category ----------

class AdminCategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminRole]


class AdminCategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminRole]


class AdminCategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminRole]


# ---------- Admin: Product ----------

class AdminProductListView(generics.ListCreateAPIView):
    """GET/POST /admin/products — Mahsulotlar ro'yxati + yangi mahsulot qo'shish (admin)."""

    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminProductSerializer
        return ProductSerializer

    def get_queryset(self):
        qs = Product.objects.all()
        category_id = self.request.query_params.get('category_id')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class AdminProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdminRole]
    parser_classes = [MultiPartParser, FormParser]


class AdminProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminRole]


class AdminProductToggleView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductToggleSerializer
    permission_classes = [IsAdminRole]


# ---------- Like / Dislike ----------

class ProductLikeToggleView(APIView):
    """
    POST /products/<pk>/like — like yoki dislike bosish.
    Body: {"is_like": true}  -> like
          {"is_like": false} -> dislike
    Agar foydalanuvchi avval xuddi shu turdagi baho qo'ygan bo'lsa,
    bosilganda u bekor qilinadi (o'chiriladi).
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        serializer = ProductLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        like, created = ProductLike.objects.get_or_create(
            product=product,
            user=request.user,
            defaults={
                "is_like": serializer.validated_data["is_like"]
            }
        )

        if not created:
            if like.is_like == serializer.validated_data["is_like"]:
                like.delete()
                return Response({
                    "message": "Removed",
                    "likes_count": product.likes.filter(is_like=True).count(),
                    "dislikes_count": product.likes.filter(is_like=False).count(),
                })
            else:
                like.is_like = serializer.validated_data["is_like"]
                like.save()

        return Response({
            "message": "Success",
            "likes_count": product.likes.filter(is_like=True).count(),
            "dislikes_count": product.likes.filter(is_like=False).count(),
        })


# ==== Menu Comment Views ====

class ProductCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductCommentCreateSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return ProductComment.objects.filter(product_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        serializer.save(product=product)


class ProductCommentDeleteView(generics.DestroyAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAdminRole]


class ProductRatingCreateView(generics.CreateAPIView):
    serializer_class = ProductRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating, created = ProductRating.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'score': serializer.validated_data['score']}
        )
        return Response({'score': rating.score}, status=status.HTTP_200_OK)


class ProductRatingDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        user = request.user if request.user.is_authenticated else None
        user_rating = None
        if user:
            r = ProductRating.objects.filter(product=product, user=user).first()
            user_rating = r.score if r else None
        all_ratings = product.ratings.all()
        avg = round(sum(r.score for r in all_ratings) / all_ratings.count(), 1) if all_ratings else None
        return Response({
            'score': user_rating,
            'average_score': avg,
            'ratings_count': all_ratings.count(),
            'likes_count': product.likes.filter(is_like=True).count(),
            'dislikes_count': product.likes.filter(is_like=False).count(),
        })
