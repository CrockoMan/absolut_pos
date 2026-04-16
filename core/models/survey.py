from django.core.exceptions import ValidationError
from django.db import models

from core.choices.role import UserRoleChoices
from core.models.base import BaseModel


class Survey(BaseModel):
    author = models.ForeignKey(
        # User,
        'core.User',
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='Автор',
        limit_choices_to={'role': UserRoleChoices.ROLE_SURVEY_ADMIN},
    )

    name = models.CharField(
        max_length=64,
        verbose_name='Название опроса',
    )

    survey_date = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        errors = {}

        if self.author.role != UserRoleChoices.ROLE_SURVEY_ADMIN:
            errors['author'] = f'{self.author.username} Не может создавать опросы'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
