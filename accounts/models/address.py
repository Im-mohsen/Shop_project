from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    # اعتبارسنجهای اختصاصی برای ایران
    phone_validator = RegexValidator(
        regex=r'^09\d{9}$',
        message=_("شماره تلفن گیرنده باید با ۰۹ شروع شده و ۱۱ رقم باشد.")
    )
    postal_code_validator = RegexValidator(
        regex=r'^\d{10}$',
        message=_("کد پستی باید دقیقاً ۱۰ رقم و بدون خط تیره باشد.")
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', verbose_name=_("کاربر"))

    province = models.CharField(max_length=100, verbose_name=_("استان"))
    city = models.CharField(max_length=100, verbose_name=_("شهر"))
    postal_code = models.CharField(
        max_length=10,
        validators=[postal_code_validator],
        verbose_name=_("کد پستی")
    )
    full_address = models.TextField(verbose_name=_("نشانی پستی دقیق"))
    plaque = models.CharField(max_length=10, verbose_name=_("پلاک"))
    unit = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("واحد"))

    receiver_name = models.CharField(max_length=255, verbose_name=_("نام و نام خانوادگی گیرنده"))
    receiver_phone = models.CharField(max_length=11, validators=[phone_validator], verbose_name=_("شماره تماس گیرنده"))

    # وضعیت‌ها و زمان‌سنجی
    is_default = models.BooleanField(default=False, verbose_name=_("آدرس پیش‌فرض"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین ویرایش"))

    class Meta:
        verbose_name = _("آدرس")
        verbose_name_plural = _("آدرس‌ها")
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.receiver_name} - {self.city}, {self.province}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)

        super().save(*args, **kwargs)