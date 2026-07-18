from django.db.models import Count, DecimalField, Sum, Value
from django.db.models.functions import Coalesce, TruncDate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.accounts.permissions import IsAdminRole
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    """POST /api/orders — Yangi buyurtma yaratish (checkout)."""

    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]


class AdminOrderListView(generics.ListAPIView):
    """GET /api/admin/orders — Barcha buyurtmalar ro'yxati (admin)."""

    queryset = Order.objects.all().prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminRole]


class AdminSalesStatsView(APIView):
    """
    GET /api/admin/stats/sales — Sana bo'yicha savdo summasi.

    Ixtiyoriy query parametrlar:
      ?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD — davr bo'yicha filtrlash
    Javob: har bir sana uchun umumiy savdo summasi va buyurtmalar soni.
    """

    permission_classes = [IsAdminRole]

    def get(self, request):
        queryset = Order.objects.exclude(status=Order.Status.CANCELLED)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        data = (
            queryset
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(
                total_sales=Coalesce(
                    Sum('total_amount'), Value(0), output_field=DecimalField()
                ),
                orders_count=Count('id'),
            )
            .order_by('-date')
        )
        return Response(list(data))


class AdminTopProductsStatsView(APIView):
    """GET /api/admin/stats/top-products — Top 5 sotilgan mahsulot."""

    permission_classes = [IsAdminRole]

    def get(self, request):
        data = (
            OrderItem.objects
            .exclude(order__status=Order.Status.CANCELLED)
            .values('product__id', 'product__name')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')[:5]
        )
        result = [
            {
                'product_id': row['product__id'],
                'product_name': row['product__name'],
                'total_quantity': row['total_quantity'],
            }
            for row in data
        ]
        return Response(result)


class AdminSalesChannelStatsView(APIView):
    """GET /api/admin/stats/sales-channel — Online/Offline sotuv foizi."""

    permission_classes = [IsAdminRole]

    def get(self, request):
        queryset = Order.objects.exclude(status=Order.Status.CANCELLED)
        total_count = queryset.count()

        channel_counts = (
            queryset.values('channel')
            .annotate(count=Count('id'))
        )
        counts_map = {row['channel']: row['count'] for row in channel_counts}
        online_count = counts_map.get(Order.Channel.ONLINE, 0)
        offline_count = counts_map.get(Order.Channel.OFFLINE, 0)

        def percent(count):
            return round((count / total_count) * 100, 2) if total_count else 0.0

        return Response({
            'total_orders': total_count,
            'online': {'count': online_count, 'percent': percent(online_count)},
            'offline': {'count': offline_count, 'percent': percent(offline_count)},
        })


class AdminOrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all().prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminRole]


class AdminOrderStatusUpdateView(APIView):
    permission_classes = [IsAdminRole]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.data.get('status')
        if new_status not in dict(Order.Status.choices):
            return Response(
                {'detail': 'Noto\'g\'ri status. Tanlov: ' + ', '.join(dict(Order.Status.choices).keys())},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = new_status
        order.save(update_fields=['status'])
        return Response(OrderSerializer(order).data)


class AdminDashboardStatsView(APIView):
    """GET /admin/stats/dashboard — Dashboard umumiy statistikasi."""

    permission_classes = [IsAdminRole]

    def get(self, request):
        from apps.menu.models import ProductRating

        active_orders = Order.objects.exclude(status=Order.Status.CANCELLED)

        total_revenue = active_orders.aggregate(
            total=Coalesce(Sum('total_amount'), Value(0), output_field=DecimalField())
        )['total']

        total_orders = active_orders.count()

        total_customers = active_orders.values('customer_phone').distinct().count()

        ratings = ProductRating.objects.all()
        if ratings.exists():
            avg_rating = round(sum(r.score for r in ratings) / ratings.count(), 1)
        else:
            avg_rating = 0

        return Response({
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'avg_rating': avg_rating,
        })
