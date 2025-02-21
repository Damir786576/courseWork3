from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=False)  # Почта должна быть подтверждена
    token = models.CharField(max_length=64, unique=True, null=True, blank=True)  # Токен для подтверждения

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(16)
        super().save(*args, **kwargs)
