from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from core.models.base import BaseModel


class SurveyResponse(BaseModel):
    # survey = models.ForeignKey(
    #     'core.Survey',
    #     on_delete=models.CASCADE,
    #     related_name='responses',
    #     verbose_name='Опрос',
    # )
    survey_question = models.ForeignKey(
        'core.SurveyQuestion',
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Опрос',
    )

    user = models.ForeignKey(
        # User,
        'core.User',
        on_delete=models.CASCADE,
        related_name='survey_responses',
        verbose_name='Пользователь',
        null=True,
        blank=True,
    )

    text = models.TextField(
        'Текст варианта'
    )

    started_at = models.DateTimeField(
        'Вопрос задан',
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        'Получен ответ',
        null=True,
        blank=True,
    )

    response_duration = models.IntegerField(
        'Длительность ответа',
        help_text='Время между началом и завершением ответа',
        default=0,
    )

    class Meta:
        verbose_name = 'Ответ на опрос'
        verbose_name_plural = 'Ответы на опросы'
        unique_together = ['user', 'survey_question',]

    def __str__(self):
        return f'{self.user.email} - {self.survey_question.text[:50]}'

    def save(self, *args, **kwargs):
        if self.pk and (self.completed_at and self.started_at):
            delta = self.completed_at - self.started_at
            self.response_duration = int(delta.total_seconds())
        else:
            self.response_duration = 0

        super().save(*args, **kwargs)
