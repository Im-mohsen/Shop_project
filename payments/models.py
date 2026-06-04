from django.db import models
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', _('در انتظار پرداخت')
        SUCCESS = 'success', _('پرداخت موفق')
        FAILED = 'failed', _('پرداخت ناموفق')
        CANCELED = 'canceled', _('لغو شده توسط کاربر')

    order = models.ForeignKey('orders.Order', on_delete=models.PROTECT, related_name='payments', verbose_name=_("سفارش"))

    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name=_("مبلغ تراکنش (ریال)"))

    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name=_("وضعیت تراکنش"))

    gateway = models.CharField(max_length=50, verbose_name=_("درگاه پرداخت"))

    authority = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("کد اتوریتی / توکن درگاه"))

    ref_id = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name=_("شماره پیگیری بانک (RefID)"))

    gateway_response = models.TextField(blank=True, null=True, verbose_name=_("پاسخ کامل درگاه (Log)"))

    paid_at = models.DateTimeField(blank=True, null=True, verbose_name=_("زمان تایید پرداخت بانک"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد تراکنش"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین ویرایش"))

    class Meta:
        verbose_name = _("تراکنش پرداخت")
        verbose_name_plural = _("تراکنش‌های پرداخت")
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['authority']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Payment {self.id} - Amount: {self.amount} ریال ({self.get_status_display()})"