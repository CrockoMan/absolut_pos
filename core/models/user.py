from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.choices.role import UserRoleChoices


class User(AbstractUser):
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=16,
        choices=UserRoleChoices,
        default=UserRoleChoices.ROLE_USER,
    )

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
