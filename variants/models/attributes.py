from django.db import models
from django.utils.translation import gettext_lazy as _


class Attribute(models.Model):
    class AttributeType(models.TextChoices):
        TEXT = 'text', _('متنی')
        COLOR = 'color', _('رنگ')
        NUMBER = 'number', _('عددی')

    title = models.CharField(max_length=255, verbose_name=_("نام ویژگی"))
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name=_("اسلاگ (URL)"))
    type = models.CharField(max_length=20, choices=AttributeType.choices, default=AttributeType.TEXT, verbose_name=_("نوع ویژگی"))
    is_filterable = models.BooleanField(default=True, verbose_name=_("قابل فیلتر است؟"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ساخت"))

    class Meta:
        verbose_name = _("ویژگی")
        verbose_name_plural = _("ویژگی‌ها")
        indexes = [
            models.Index(fields=['is_filterable']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values', verbose_name=_("ویژگی مربوطه"))
    value = models.CharField(max_length=255, verbose_name=_("مقدار"))
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name=_("اسلاگ (URL)"))

    color_code = models.CharField(max_length=7, blank=True, null=True, help_text=_("کد هگزادسیمال رنگ مثل #FFFFFF"), verbose_name=_("کد رنگ"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ساخت"))

    class Meta:
        verbose_name = _("مقدار ویژگی")
        verbose_name_plural = _("مقادیر ویژگی‌ها")

    def __str__(self):
        return f"{self.attribute.title}: {self.value}"
