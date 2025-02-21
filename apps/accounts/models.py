from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from .manager import MyUserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    phone_regex = RegexValidator(
        regex=r'^((\+7)|8)\d{10}$',
        message="Номер телефона должен быть в формате: '+79999999999' или '89999999999'. Допускается до 12 цифр.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=12, null=True, blank=True)

    user_manager = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
