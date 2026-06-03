from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('Phone number is required'))

        phone = phone.strip()

        extra_fields.setdefault('is_active', True)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True, verbose_name=_("تلفن همراه"))
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_("آدرس ایمیل"))
    first_name = models.CharField(max_length=150, blank=True, verbose_name=_("نام"))
    last_name = models.CharField(max_length=150, blank=True, verbose_name=_("نام خانوادگی"))

    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))
    is_staff = models.BooleanField(default=False, verbose_name=_("کارمند / دسترسی به ادمین"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ عضویت"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین ویرایش"))

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _("کاربر")
        verbose_name_plural = _("کاربران")

    def __str__(self):
        return f"{self.phone} - {self.first_name} {self.last_name}"