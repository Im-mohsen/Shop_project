from django.contrib import admin
from .models import Attribute, AttributeValue, ProductVariant, VariantAttributeValue


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1
    fields = ['value', 'slug', 'color_code']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'is_filterable', 'created_at']
    list_filter = ['type', 'is_filterable']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AttributeValueInline]


class VariantAttributeValueInline(admin.TabularInline):
    model = VariantAttributeValue
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'sku', 'price', 'discount_price', 'stock_quantity', 'is_active']
    list_filter = ['is_active', 'created_at', 'product__brand', 'product__category']
    search_fields = ['sku', 'barcode', 'product__title']
    list_editable = ['price', 'discount_price', 'stock_quantity', 'is_active']
    inlines = [VariantAttributeValueInline]

    raw_id_fields = ['product']