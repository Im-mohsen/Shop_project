from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts', blank=True, null=True, verbose_name=_("کاربر"))
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name=_("کلید نشست (Session)"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ساخت"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین تغییر"))

    class Meta:
        verbose_name = _("سبد خرید")
        verbose_name_plural = _("سبدهای خرید")

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        if self.user:
            return f"Cart for User: {self.user.phone}"
        return f"Guest Cart: {self.session_key[:8] if self.session_key else 'Unknown'}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name=_("سبد خرید"))
    variant = models.ForeignKey('variants.ProductVariant', on_delete=models.CASCADE, related_name='cart_items', verbose_name=_("تنوع محصول"))
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_("تعداد"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ اضافه شدن"))

    class Meta:
        verbose_name = _("آیتم سبد خرید")
        verbose_name_plural = _("آیتم‌های سبد خرید")
        unique_together = ('cart', 'variant')

    def __str__(self):
        return f"{self.quantity} x {self.variant.sku}"

    @property
    def total_price(self):
        price_to_use = self.variant.discount_price if self.variant.discount_price else self.variant.price
        return price_to_use * self.quantity