from django.contrib import admin
from .models import Coupon, CouponUsage


class CouponUsageInline(admin.TabularInline):
    model = CouponUsage
    extra = 0
    raw_id_fields = ['user', 'order']
    readonly_fields = ['user', 'order', 'discount_amount', 'used_at']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'type', 'value', 'is_valid_status', 'used_count', 'max_usage', 'expire_at',
                    'is_active']
    list_filter = ['type', 'is_active', 'start_date', 'expire_at']
    search_fields = ['code', 'title']
    list_editable = ['is_active']
    inlines = [CouponUsageInline]

    def is_valid_status(self, obj):
        return obj.is_valid

    is_valid_status.boolean = True
    is_valid_status.short_description = "وضعیت اعتبار فعلی"