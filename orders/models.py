from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', _('در انتظار پرداخت')
        PAID = 'paid', _('پرداخت شده / در حال پردازش')
        SHIPPED = 'shipped', _('تحویل به پست / ارسال شده')
        DELIVERED = 'delivered', _('تحویل داده شده')
        CANCELED = 'canceled', _('لغو شده')
        REFUNDED = 'refunded', _('مرجوع شده')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders', verbose_name=_("کاربر"))
    address = models.ForeignKey('accounts.Address', on_delete=models.SET_NULL, blank=True, null=True, related_name='orders', verbose_name=_("نشانی ارسال"))
    # coupon = models.ForeignKey('discounts.Coupon', on_delete=models.SET_NULL, blank=True, null=True, related_name='orders', verbose_name=_("کد تخفیف استفاده شده"))

    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name=_("وضعیت سفارش"))
    tracking_code = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name=_("کد رهگیری پستی"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات کاربر / ادمین"))

    total_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_("مجموع قیمت اقلام"))
    shipping_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name=_("هزینه ارسال"))
    discount_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name=_("مبلغ تخفیف کد"))
    final_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_("مبلغ قابل پرداخت نهایی"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت سفارش"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین تغییر وضعیت"))

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارشات")
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"Order #{self.id} - User: {self.user.phone} ({self.get_status_display()})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("سفارش مربوطه"))
    variant = models.ForeignKey('variants.ProductVariant', on_delete=models.PROTECT, related_name='order_items', verbose_name=_("تنوع محصول خریده شده"))

    quantity = models.PositiveIntegerField(default=1, verbose_name=_("تعداد"))

    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_("قیمت واحد در لحظه خرید"))
    total_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_("قیمت کل این آیتم"))

    class Meta:
        verbose_name = _("آیتم سفارش")
        verbose_name_plural = _("آیتم‌های سفارش")

    def __str__(self):
        return f"{self.quantity} x variant {self.variant_id} (Order #{self.order_id})"