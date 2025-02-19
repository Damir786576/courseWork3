from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=255,
        verbose_name="username"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="email"
    )
    phone_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Введите номер телефона"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )
    country = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Введите страну проживания"
    )
    token = models.CharField(
        unique=True,
        null=True,
        blank=True,
        max_length=255  # Указываем max_length
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_block_user", "Сan block user"),
        ]
