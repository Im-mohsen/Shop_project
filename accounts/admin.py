from django.contrib import admin
from .models import User, Address


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    fieldsets = [
        (None, {'fields': ('title', 'receiver_name', 'receiver_phone')}),
        ('نشانی', {'fields': ('province', 'city', 'postal_code', 'address_detail')}),
    ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at']
    list_filter = ['is_staff', 'is_active', 'created_at']
    search_fields = ['phone', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    inlines = [AddressInline]

    readonly_fields = ['created_at', 'last_login']