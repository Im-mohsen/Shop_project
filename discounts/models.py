from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    class CouponType(models.TextChoices):
        PERCENTAGE = 'percentage', _('درصدی')
        FIXED_AMOUNT = 'fixed_amount', _('مبلغ ثابت')

    code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name=_("کد تخفیف"))
    title = models.CharField(max_length=255, verbose_name=_("عنوان / مناسبت"))

    type = models.CharField(max_length=20, choices=CouponType.choices, default=CouponType.PERCENTAGE, verbose_name=_("نوع تخفیف"))

    value = models.PositiveIntegerField(verbose_name=_("مقدار تخفیف (درصد یا ریال)"))

    max_discount = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True, verbose_name=_("سقف تخفیف (ریال) - مخصوص درصدی"))
    min_order_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name=_("حداقل مبلغ سفارش برای اعمال کد (ریال)"))

    max_usage = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("حداکثر تعداد دفعات استفاده کل"))
    used_count = models.PositiveIntegerField(default=0, verbose_name=_("تعداد دفعات استفاده شده"))

    start_date = models.DateTimeField(verbose_name=_("تاریخ شروع اعتبار"))
    expire_at = models.DateTimeField(verbose_name=_("تاریخ انقضا"))

    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ساخت"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین تغییر"))

    class Meta:
        verbose_name = _("کد تخفیف")
        verbose_name_plural = _("کدهای تخفیف")
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['is_active', 'start_date', 'expire_at']),
        ]

    def __str__(self):
        return f"{self.code} ({self.get_type_display()})"

    @property
    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if not (self.start_date <= now <= self.expire_at):
            return False
        if self.max_usage and self.used_count >= self.max_usage:
            return False
        return True


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages', verbose_name=_("کد تخفیف"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coupon_usages', verbose_name=_("کاربر استفاده‌کننده"))
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='coupon_usages', verbose_name=_("سفارش مربوطه"))

    discount_amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_("مبلغ تخفیف کسر شده (ریال)"))
    used_at = models.DateTimeField(auto_now_add=True, verbose_name=_("زمان استفاده"))

    class Meta:
        verbose_name = _("تاریخچه استفاده از تخفیف")
        verbose_name_plural = _("تاریخچه‌های استفاده از تخفیف")

        unique_together = ('coupon', 'user')
        indexes = [
            models.Index(fields=['coupon', 'user']),
        ]

    def __str__(self):
        return f"User {self.user_id} used {self.coupon.code} on Order {self.order_id}"