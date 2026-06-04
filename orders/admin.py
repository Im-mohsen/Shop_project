from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['variant']
    readonly_fields = ['variant', 'quantity', 'price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'final_price', 'tracking_code', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['id', 'user__phone', 'tracking_code']
    list_editable = ['status', 'tracking_code']
    raw_id_fields = ['user', 'address', 'coupon']
    inlines = [OrderItemInline]

    readonly_fields = ['total_price', 'shipping_price', 'discount_amount', 'final_price', 'created_at', 'updated_at']