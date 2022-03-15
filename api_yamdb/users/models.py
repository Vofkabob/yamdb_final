import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_me


class User(AbstractUser):
    """
    Кастомизированная модель пользователя.
    """
    REQUIRED_FIELDS = ['email']

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [(USER, 'Пользователь'),
                    (MODERATOR, 'Модератор'),
                    (ADMIN, 'Администратор')]

    role = models.CharField(
        verbose_name='Роль',
        max_length=9,
        choices=ROLE_CHOICES,
        blank=False,
        default=USER)

    bio = models.TextField(
        verbose_name='Биография',
        blank=True)

    email = models.EmailField(
        verbose_name='Электронная почта',
        blank=False,
        unique=True)

    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        blank=False,
        max_length=150,
        validators=[validate_me])

    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=36,
        null=True,
        blank=True)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @staticmethod
    def generate_code():
        return uuid.uuid4().hex

    class Meta:
        ordering = ['username']
