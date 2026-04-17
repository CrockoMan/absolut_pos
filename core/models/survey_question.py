from django.db import models
from core.models.base import BaseModel


class SurveyQuestion(BaseModel):
    survey = models.ForeignKey(
        'core.Survey',
        on_delete=models.CASCADE,
        related_name='survey_questions',
        verbose_name='Опрос',
        null=True,
        blank=True,
    )
    text = models.TextField('Текст вопроса')
    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order', ]

    def __str__(self):
        if self.survey and self.survey.name:
            return f'{self.survey.name} - {self.text[:50]}'
        return f'Вопрос без опроса: {self.text[:50]}'