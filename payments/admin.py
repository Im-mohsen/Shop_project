from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'gateway', 'status', 'ref_id', 'paid_at', 'created_at']
    list_filter = ['status', 'gateway', 'created_at', 'paid_at']
    search_fields = ['id', 'authority', 'ref_id', 'order__id', 'order__user__phone']
    list_editable = [
        'status']
    raw_id_fields = ['order']

    readonly_fields = ['order', 'amount', 'gateway', 'authority', 'ref_id', 'gateway_response', 'paid_at', 'created_at',
                       'updated_at']