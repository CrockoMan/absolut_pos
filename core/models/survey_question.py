from django.db import models
from core.models.base import BaseModel


class SurveyQuestion(BaseModel):
    survey = models.ForeignKey(
        'core.Survey',
        on_delete=models.CASCADE,
        related_name='survey_items',
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
        unique_together = (('survey', 'text'),)

    def __str__(self):
        return f'{self.survey.name}  {self.text[:50]}'
