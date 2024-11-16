from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        blank=True,
        null=True,
        help_text="Введите Ваше имя",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        blank=True,
        null=True,
        help_text="Введите Вашу фамилию",
    )
    phone_number = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите Ваш аватар",
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Стана проживания",
        blank=True,
        null=True,
        help_text="Введите Вашу страну проживания",
    )
    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Токен пользователя")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("can_block_user", "can block user")]

    def __str__(self):
        return f"{self.first_name} {self.last_name}, e-mail: {self.email}, разблокирован: {self.is_active}"


# Create your models here.
