from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import Category, Brand, Tag


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name=_("دسته بندی"))
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name=_("برند"))
    tags = models.ManyToManyField(Tag, through='ProductTag', related_name='products', verbose_name=_("تگ‌ها"))

    title = models.CharField(max_length=255, verbose_name=_("نام محصول"))
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name=_("اسلاگ (URL)"))
    short_description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات کوتاه"))
    description = models.TextField(verbose_name=_("توضیحات اصلی"))
    weight = models.PositiveIntegerField(default=0, help_text=_("وزن به گرم"), verbose_name=_("وزن"))
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("تعداد بازدید"))

    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))
    is_featured = models.BooleanField(default=False, verbose_name=_("پیشنهاد ویژه"))

    meta_title = models.CharField(max_length=120, blank=True, null=True, verbose_name=_("متای عنوان"))
    meta_description = models.TextField(max_length=200, blank=True, null=True, verbose_name=_("متای توضیحات"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین به‌روزرسانی"))

    class Meta:
        verbose_name = _("محصول")
        verbose_name_plural = _("محصولات")
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['-created_at']),

            models.Index(fields=['is_active']),

            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_("محصول"))
    image = models.ImageField(upload_to='products/gallery/', verbose_name=_("تصویر"))
    alt_text = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("متن جایگزین (Alt)"))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("ترتیب نمایش"))
    is_main = models.BooleanField(default=False, verbose_name=_("تصویر اصلی"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت"))

    class Meta:
        verbose_name = _("تصویر محصول")
        verbose_name_plural = _("تصاویر محصولات")
        ordering = ['sort_order', '-created_at']

        indexes = [
            models.Index(fields=['product', 'sort_order']),
        ]


class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("محصول"))
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name=_("تگ"))

    class Meta:
        verbose_name = _("تگ محصول")
        verbose_name_plural = _("تگ‌های محصولات")
        unique_together = ('product', 'tag')

    def __str__(self):
        return f"{self.product.title} - {self.tag.title}"
