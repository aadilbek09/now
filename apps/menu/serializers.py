from rest_framework import serializers

from .models import Category, Product, ProductComment, ProductLike, ProductRating


# ---------- Category ----------

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'order')


# ---------- Product ----------

class ProductSerializer(serializers.ModelSerializer):
    """
    Mahsulotni to'liq ko'rsatish uchun (list, detail, admin create/update).
    Frontendda ko'rsatiladigan qo'shimcha statistikalar
    (yulduzcha, like/dislike, izohlar soni) ham shu yerda hisoblab beriladi.
    """

    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'category_name',
            'name',
            'description',
            'price',
            'image',
            'is_active',
            'is_popular',
            'created_at',
            'average_rating',
            'ratings_count',
            'likes_count',
            'dislikes_count',
            'comments_count',
        )

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if not ratings:
            return None
        return round(sum(r.score for r in ratings) / ratings.count(), 1)

    def get_ratings_count(self, obj):
        return obj.ratings.count()

    def get_likes_count(self, obj):
        return obj.likes.filter(is_like=True).count()

    def get_dislikes_count(self, obj):
        return obj.likes.filter(is_like=False).count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class ProductToggleSerializer(serializers.ModelSerializer):
    """
    Admin mahsulotni faol/nofaol qilish uchun — faqat is_active maydoni
    bilan ishlaydi (AdminProductToggleView shu orqali PATCH qabul qiladi).
    """

    class Meta:
        model = Product
        fields = ('is_active',)


class AdminProductSerializer(serializers.ModelSerializer):
    """Admin uchun mahsulot qo'shish/tahrirlash (FormData bilan)."""

    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'category_name',
                  'image', 'is_active', 'is_popular', 'created_at')
        read_only_fields = ('id', 'created_at')


# ---------- Comment ----------

class ProductCommentCreateSerializer(serializers.ModelSerializer):
    """
    Izoh qoldirish uchun — product maydoni view ichida
    (perform_create'da) avtomatik qo'yiladi, shuning uchun bu yerda yo'q.
    """

    class Meta:
        model = ProductComment
        fields = ('id', 'text', 'created_at')
        read_only_fields = ('id', 'created_at')


class ProductCommentSerializer(serializers.ModelSerializer):
    """To'liq ko'rinish — admin uchun (o'chirish, ro'yxat)."""

    class Meta:
        model = ProductComment
        fields = ('id', 'product', 'text', 'created_at')


# ---------- Like / Dislike ----------

class ProductLikeSerializer(serializers.Serializer):
    """
    ProductLikeToggleView faqat is_like qiymatini tekshirish uchun
    ishlatadi — model bilan bog'liq emas, shuning uchun oddiy Serializer.
    """

    is_like = serializers.BooleanField()


# ---------- Rating ----------

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ('id', 'product', 'user', 'score')
        read_only_fields = ('id', 'product', 'user')

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Baho 1 dan 5 gacha bo'lishi kerak.")
        return value
