from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'channel', 'status', 'total_amount', 'created_at')
    list_filter = ('channel', 'status', 'created_at')
    search_fields = ('customer_name', 'customer_phone')
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount',)
