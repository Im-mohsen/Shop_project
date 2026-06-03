from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children', verbose_name=_("دسته بندی مادر"))
    title = models.CharField(max_length=255, verbose_name=_("عنوان"))
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name=_("اسلاگ (URL)"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name=_("تصویر"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))

    meta_title = models.CharField(max_length=120, blank=True, null=True, verbose_name=_("متای عنوان"))
    meta_description = models.TextField(max_length=200, blank=True, null=True, verbose_name=_("متای توضیحات"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ساخت"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین تغییر"))

    class Meta:
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی‌ها")

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("نام برند"))
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name=_("اسلاگ (URL)"))
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))

    meta_title = models.CharField(max_length=120, blank=True, null=True, verbose_name=_("متای عنوان"))
    meta_description = models.TextField(max_length=200, blank=True, null=True, verbose_name=_("متای توضیحات"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ساخت"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین تغییر"))

    class Meta:
        verbose_name = _("برند")
        verbose_name_plural = _("برندها")

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("عنوان تگ"))
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name=_("اسلاگ (URL)"))

    class Meta:
        verbose_name = _("تگ")
        verbose_name_plural = _("تگ‌ها")

    def __str__(self):
        return self.title
