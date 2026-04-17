from collections import Counter

from django.db.models import Avg
from django.db.models import Count
from django.db.models import FloatField
from django.db.models import Sum
from django.db.models import Value
from django.db.models.functions import Coalesce
from django.db.models.functions import Round
from import_export import fields
from import_export import resources
from import_export.widgets import DateWidget

from core.models import Survey
from core.models import SurveyResponse


class SurveyResource(resources.ModelResource):
    author = fields.Field(
        column_name='Автор',
        attribute='author',
    )
    name = fields.Field(
        column_name='Название опроса',
        attribute='name',
    )
    survey_date = fields.Field(
        column_name='Дата создания',
        attribute='survey_date',
        widget=DateWidget(format='%d.%m.%Y')
    )

    questions_count = fields.Field(
        column_name='Количество вопросов',
        attribute='questions_count',
        readonly=True
    )
    questions_list = fields.Field(
        column_name='Список вопросов',
        attribute='questions_list',
        readonly=True
    )
    responses_count = fields.Field(
        column_name='Количество ответов',
        attribute='responses_count',
        readonly=True
    )
    unique_users_count = fields.Field(
        column_name='Уникальных пользователей',
        attribute='unique_users_count',
        readonly=True
    )
    avg_completion_time_minutes = fields.Field(
        column_name='Среднее время прохождения (минут)',
        attribute='avg_completion_time_minutes',
        readonly=True
    )
    popular_answers = fields.Field(
        column_name='Популярные ответы',
        attribute='popular_answers',
        readonly=True
    )

    def dehydrate_author(self, survey):
        return survey.author.username if survey.author else ''

    def dehydrate_questions_count(self, survey):
        return survey.survey_questions.count()

    def dehydrate_questions_list(self, survey):
        questions = survey.survey_questions.all().order_by('order')
        return '; '.join([f"{q.order}. {q.text}" for q in questions])

    def dehydrate_responses_count(self, survey):
        if hasattr(survey, 'total_responses'):
            return survey.total_responses
        return SurveyResponse.objects.filter(
            survey_question__survey=survey
        ).count()

    def dehydrate_unique_users_count(self, survey):
        if hasattr(survey, 'unique_users'):
            return survey.unique_users
        return SurveyResponse.objects.filter(
            survey_question__survey=survey
        ).values('user').distinct().count()

    def dehydrate_avg_completion_time_minutes(self, survey):
        if hasattr(survey, 'avg_completion_minutes'):
            return survey.avg_completion_minutes
        responses = SurveyResponse.objects.filter(
            survey_question__survey=survey
        )

        user_times = responses.values('user').annotate(
            total_time=Sum('response_duration')
        ).filter(total_time__gt=0)

        if not user_times:
            return 0

        avg_time_seconds = sum(item['total_time'] for item in user_times) / len(user_times)
        avg_time_minutes = round(avg_time_seconds / 60, 1)

        return avg_time_minutes

    def dehydrate_popular_answers(self, survey):
        responses = SurveyResponse.objects.filter(
            survey_question__survey=survey
        ).select_related('survey_question', 'survey_question_item')

        if not responses.exists():
            return "Нет ответов"

        answers_by_question = {}

        for response in responses:
            question_text = response.survey_question.text
            answer_text = response.survey_question_item.text if response.survey_question_item else response.text

            if not answer_text:
                answer_text = "(пустой ответ)"

            if question_text not in answers_by_question:
                answers_by_question[question_text] = Counter()

            answers_by_question[question_text][answer_text] += 1

        popular_answers_list = []

        for question_text, answers_counter in answers_by_question.items():
            top_answers = answers_counter.most_common(3)

            if top_answers:
                answers_str = ', '.join([f'{answer} ({count} раз)' for answer, count in top_answers])
                short_question = question_text[:50] + '...' if len(question_text) > 50 else question_text
                popular_answers_list.append(f'"{short_question}": {answers_str}')

        if not popular_answers_list:
            return '-'

        result = '; '.join(popular_answers_list)
        if len(result) > 1000:
            result = result[:997] + '...'

        return result

    class Meta:
        model = Survey
        fields = (
            'id',
            'name',
            'author',
            'survey_date',
            'questions_count',
            'responses_count',
            'unique_users_count',
            'avg_completion_time_minutes',
            'popular_answers',
            'questions_list',
        )
        export_order = (
            'id',
            'name',
            'author',
            'survey_date',
            'questions_count',
            'responses_count',
            'unique_users_count',
            'avg_completion_time_minutes',
            'questions_list',
            'popular_answers',
        )

    def get_export_queryset(self, request):
        return super().get_export_queryset(request).annotate(
            total_responses=Count('survey_questions__responses', distinct=True),
            unique_users=Count('survey_questions__responses__user', distinct=True),
            avg_completion_minutes=Coalesce(
                Round(
                    Avg('survey_questions__responses__response_duration') / 60,
                    1
                ),
                Value(0, output_field=FloatField())
            )
        ).order_by('-survey_date')
