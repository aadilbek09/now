from django.db import transaction
from rest_framework import serializers

from apps.menu.models import Product
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_name', 'product_image', 'product_price', 'quantity', 'subtotal')

    def get_product_price(self, obj):
        return float(obj.product.price)

    def get_subtotal(self, obj):
        return float(obj.subtotal)


class CartAddItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Bunday faol mahsulot topilmadi.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total', 'created_at', 'updated_at')

    def get_total(self, obj):
        return float(obj.total())


class OrderItemCreateSerializer(serializers.Serializer):
    """Checkout paytida yuboriladigan bitta mahsulot elementi."""

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Bunday faol mahsulot topilmadi.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price', 'subtotal')
        read_only_fields = ('id', 'price', 'subtotal')


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    POST /api/orders — Yangi buyurtma yaratish (checkout).
    Mijoz mahsulot(lar) ro'yxatini yuboradi, narx serverda hisoblanadi.
    """

    items = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'customer_name', 'customer_last_name', 'customer_phone',
            'address', 'channel',
            'status', 'total_amount', 'created_at', 'items',
        )
        read_only_fields = ('id', 'status', 'total_amount', 'created_at')

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Buyurtmada kamida bitta mahsulot bo'lishi kerak.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        order_items = []
        for item in items_data:
            product = Product.objects.get(id=item['product_id'])
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                )
            )
        OrderItem.objects.bulk_create(order_items)
        order.recalculate_total()
        return order


class OrderSerializer(serializers.ModelSerializer):
    """GET /api/admin/orders — Admin uchun buyurtma ma'lumotlari."""

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'customer_name', 'customer_last_name', 'customer_phone',
            'address', 'channel',
            'status', 'total_amount', 'created_at', 'items',
        )
        read_only_fields = fields
