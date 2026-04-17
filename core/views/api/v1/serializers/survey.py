from django.db import transaction
from rest_framework import serializers

from core.models import Survey
from core.models import SurveyQuestion
from core.views.api.v1.serializers.base import BaseModelSerializer
from core.views.api.v1.serializers.survey_question import SurveyQuestionSerializer


class SurveySerializer(BaseModelSerializer):
    """Сериализатор опросов."""
    questions = SurveyQuestionSerializer(many=True, source='survey_questions')
    id = serializers.IntegerField(required=False)

    class Meta(BaseModelSerializer.Meta):
        model = Survey
        fields = (
            'id',
            'author',
            'name',
            'survey_date',
            'questions',
        )

    def _proceed_data(self, survey, questions_data, create=False):
        """Обработка вопросов опроса."""
        processed_question_ids = []

        for question_data in questions_data:
            question_data_copy = question_data.copy()
            items_data = question_data_copy.pop('survey_question_items', [])
            question_data_copy['survey'] = survey

            if create:
                question_data_copy.pop('id', None)
                question = SurveyQuestion.objects.create(**question_data_copy)
                created = True
            else:
                question, created = SurveyQuestion.objects.update_or_create(
                    id=question_data_copy.get('id'),
                    defaults=question_data_copy
                )
            processed_question_ids.append(question.id)

            if items_data:
                SurveyQuestionSerializer()._proceed_items(question, items_data, create=create)
            else:
                question.survey_question_items.all().delete()

        if processed_question_ids:
            SurveyQuestion.objects.filter(
                survey=survey
            ).exclude(id__in=processed_question_ids).delete()
        else:
            survey.survey_questions.all().delete()

        return survey

    def validate(self, obj):
        user = self.context['request'].user
        author = obj.get('author')

        if author != user and not user.is_admin:
            raise serializers.ValidationError({'author': 'Изменение автора запрещено'})

        return obj

    @transaction.atomic
    def create(self, validated_data):
        questions_data = validated_data.pop('survey_questions', [])
        survey = Survey.objects.create(**validated_data)
        survey = Survey.objects.select_for_update(nowait=True).get(pk=survey.pk)

        if questions_data:
            self._proceed_data(survey, questions_data, create=True)

        return survey

    @transaction.atomic
    def update(self, instance, validated_data):
        questions_data = validated_data.pop('survey_questions', [])

        instance = Survey.objects.select_for_update(nowait=True).get(pk=instance.pk)
        instance.author = validated_data.get('author', instance.author)
        instance.name = validated_data.get('name', instance.name)
        instance.survey_date = validated_data.get('survey_date', instance.survey_date)
        instance.save()

        if questions_data:
            self._proceed_data(instance, questions_data)
        else:
            instance.survey_questions.all().delete()

        instance.refresh_from_db()
        return instance
