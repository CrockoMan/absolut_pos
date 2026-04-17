from django.db import models

from core.models.base import BaseModel


class SurveyQuestionItem(BaseModel):
    survey_question = models.ForeignKey(
        'core.SurveyQuestion',
        on_delete=models.CASCADE,
        related_name='survey_question_items',
        verbose_name='Вопрос',
        null=True,
        blank=True,
    )
    text = models.TextField('Вариант ответа')
    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order', ]

    def __str__(self):
        return f'{self.survey_question}  {self.text[:50]}'
