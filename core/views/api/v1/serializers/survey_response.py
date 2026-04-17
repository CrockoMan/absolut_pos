from rest_framework import serializers
from django.utils import timezone
from django.db import transaction

from core.models import Survey, SurveyQuestion, SurveyQuestionItem, SurveyResponse


class SurveyQuestionItemSerializer(serializers.ModelSerializer):
    """Варианты ответа"""

    class Meta:
        model = SurveyQuestionItem
        fields = ['id', 'text']


class SurveyResponseQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор вопроса с вариантами ответов"""
    items = serializers.SerializerMethodField()

    class Meta:
        model = SurveyQuestion
        fields = ['id', 'text', 'items']

    def get_items(self, obj):
        items = obj.survey_question_items.all()
        return SurveyQuestionItemSerializer(items, many=True).data


class SurveyResponseSerializer(serializers.ModelSerializer):
    """Сериализатор опроса"""

    class Meta:
        model = Survey
        fields = ['id', 'name']


class SubmitAnswerSerializer(serializers.Serializer):
    """Сериализатор для отправки ответа с полной валидацией"""
    current_question_id = serializers.IntegerField(required=True)
    answer_id = serializers.IntegerField(required=False, allow_null=True)
    custom_answer = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def validate_current_question_id(self, value):
        """Валидация ID вопроса"""
        if not self.survey:
            raise serializers.ValidationError('Опрос не указан')

        try:
            question = self.survey.survey_questions.get(id=value)
            self.context['question'] = question
            return value
        except SurveyQuestion.DoesNotExist:
            raise serializers.ValidationError(f'Вопрос с id={value} не найден в этом опросе {self.survey.id}')

    def validate(self, data):
        answer_id = data.get('answer_id')
        custom_answer = data.get('custom_answer', '').strip()

        if not answer_id and not custom_answer:
            raise serializers.ValidationError('Нельзя указывать оба варианта')

        if answer_id and custom_answer:
            raise serializers.ValidationError('Нельзя указывать одновременно answer_id и custom_answer')

        if answer_id:
            try:
                question_item = SurveyQuestionItem.objects.get(id=answer_id)
                data['question_item_obj'] = question_item
            except SurveyQuestionItem.DoesNotExist:
                raise serializers.ValidationError(f'Вариант ответа с id={answer_id} не существует')

        if self.user and hasattr(self, 'context') and 'question' in self.context:
            try:
                response = SurveyResponse.objects.get(
                    survey_question=self.context['question'],
                    user=self.user,
                    completed_at__isnull=True
                )
                self.context['response'] = response
            except SurveyResponse.DoesNotExist:
                raise serializers.ValidationError(
                    'Не найден активный ответ на этот вопрос. Возможно, вы уже ответили на него.'
                )

        return data

    def save(self, **kwargs):
        with transaction.atomic():
            response = self.context['response']
            question_item = self.validated_data.get('question_item_obj')
            custom_answer = self.validated_data.get('custom_answer', '').strip()

            response.completed_at = timezone.now()

            if question_item:
                response.survey_question_item = question_item
                response.text = question_item.text
            elif custom_answer:
                response.survey_question_item = None
                response.text = custom_answer

            response.save()

            return response


class SurveyOneQuestionSerializer(serializers.Serializer):
    """Сериализатор опроса"""

    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if not self.survey:
            raise serializers.ValidationError('Опрос не найден')

        if not self.user:
            raise serializers.ValidationError('Пользователь не авторизован')

        return data

    def get_current_question(self):
        all_questions = self.survey.survey_questions.all()

        if not all_questions.exists():
            raise serializers.ValidationError(
                "No questions found for this survey"
            )

        answered_question_ids = SurveyResponse.objects.filter(
            survey_question__survey=self.survey,
            user=self.user,
            completed_at__isnull=False
        ).values_list('survey_question_id', flat=True).distinct()

        current_question = None
        for question in all_questions:
            if question.id not in answered_question_ids:
                current_question = question
                break

        if current_question is None:
            raise serializers.ValidationError('Опрос пройден, отвечены все вопросы')

        return current_question

    def get_or_create_response(self, question):
        response, created = SurveyResponse.objects.get_or_create(
            survey_question=question,
            user=self.user,
            defaults={
                'survey_question_item': question.survey_question_items.first(),
                'text': '',
                'completed_at': None,
                'started_at': timezone.now(),
            }
        )
        return response

    def to_representation(self, instance):
        current_question = self.get_current_question()
        response = self.get_or_create_response(current_question)

        question_serializer = SurveyResponseQuestionSerializer(current_question)

        return {
            'survey_id': self.survey.id,
            'response_id': response.id,
            'survey_name': self.survey.name,
            'current_question': question_serializer.data,
        }
