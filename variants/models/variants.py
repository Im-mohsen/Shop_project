from django.db import models
from django.utils.translation import gettext_lazy as _
from .attributes import AttributeValue


class ProductVariant(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='variants', verbose_name=_("محصول"))
    attribute_values = models.ManyToManyField(AttributeValue, through='VariantAttributeValue', related_name='variants', verbose_name=_("ویژگی‌های این تنوع"))

    sku = models.CharField(max_length=100, unique=True, verbose_name=_("شناسه کالا (SKU)"))
    barcode = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name=_("بارکد"))

    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name=_("قیمت اصلی (ریال/تومان)"))
    discount_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name=_("قیمت با تخفیف"))

    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_("موجودی انبار"))
    weight = models.PositiveIntegerField(blank=True, null=True, help_text=_("وزن مخصوص این تنوع به گرم"),
                                         verbose_name=_("وزن"))
    image = models.ImageField(upload_to='variants/', blank=True, null=True, verbose_name=_("تصویر اختصاصی تنوع"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین به‌روزرسانی"))

    class Meta:
        verbose_name = _("تنوع محصول")
        verbose_name_plural = _("تنوع‌های محصولات")
        ordering = ['price']

        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['is_active', 'stock_quantity']),
        ]

    def __str__(self):
        return f"{self.product.title} - SKU: {self.sku}"


class VariantAttributeValue(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name=_("تنوع محصول"))
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, verbose_name=_("مقدار ویژگی"))

    class Meta:
        verbose_name = _("ویژگی تنوع محصول")
        verbose_name_plural = _("ویژگی‌های تنوع‌های محصولات")
        unique_together = ('variant', 'attribute_value')

        indexes = [
            models.Index(fields=['attribute_value', 'variant']),
        ]

    def __str__(self):
        return f"{self.variant.sku} -> {self.attribute_value}"
