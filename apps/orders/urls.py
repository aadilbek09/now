from django.urls import path

from .views import (
    AdminDashboardStatsView,
    AdminOrderDetailView,
    AdminOrderListView,
    AdminOrderStatusUpdateView,
    AdminSalesChannelStatsView,
    AdminSalesStatsView,
    AdminTopProductsStatsView,
    CartAddItemView,
    CartDetailView,
    CartRemoveItemView,
    CartUpdateItemView,
    OrderCreateView,
    UserOrderListView,
)

urlpatterns = [
    # Cart
    path('cart', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add', CartAddItemView.as_view(), name='cart-add'),
    path('cart/item/<int:pk>', CartUpdateItemView.as_view(), name='cart-update-item'),
    path('cart/item/<int:pk>/delete', CartRemoveItemView.as_view(), name='cart-remove-item'),
    # Orders
    path('orders', OrderCreateView.as_view(), name='order-create'),
    path('orders/my', UserOrderListView.as_view(), name='user-orders'),
    path('admin/orders', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/orders/<int:pk>', AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('admin/orders/<int:pk>/status', AdminOrderStatusUpdateView.as_view(), name='admin-order-status'),
    path('admin/stats/dashboard', AdminDashboardStatsView.as_view(), name='admin-stats-dashboard'),
    path('admin/stats/sales', AdminSalesStatsView.as_view(), name='admin-stats-sales'),
    path('admin/stats/top-products', AdminTopProductsStatsView.as_view(), name='admin-stats-top-products'),
    path('admin/stats/sales-channel', AdminSalesChannelStatsView.as_view(), name='admin-stats-sales-channel'),
]
