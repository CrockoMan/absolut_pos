from rest_framework import serializers

from core.models import SurveyQuestion
from core.models import SurveyQuestionItem
from core.views.api.v1.serializers.common import SurveyQuestionBase
from core.views.api.v1.serializers.survey_question_item import SurveyQuestionItemSerializer


class SurveyQuestionSerializer(SurveyQuestionBase):
    """Сериализатор для вопросов."""
    questions = SurveyQuestionItemSerializer(many=True, source='survey_question_items')
    id = serializers.IntegerField(required=False)

    class Meta(SurveyQuestionBase.Meta):
        model = SurveyQuestion
        fields = SurveyQuestionBase.Meta.fields + ('questions',)

    def _proceed_items(self, question, items_data, create=False):
        """Обновление элементов вопроса."""
        processed_item_ids = []

        for item_data in items_data:
            item_data_copy = item_data.copy()

            if create:
                item_data_copy.pop('id', None)
                question_item = SurveyQuestionItem.objects.create(
                    survey_question=question,
                    **item_data_copy
                )
            else:
                question_item, _ = SurveyQuestionItem.objects.update_or_create(
                    id=item_data_copy.get('id'),
                    defaults={
                        'survey_question': question,
                        'text': item_data_copy.get('text'),
                        'order': item_data_copy.get('order', 0),
                    }
                )

            processed_item_ids.append(question_item.id)

        # Удаляем элементы, которые не были обработаны
        SurveyQuestionItem.objects.filter(
            survey_question=question
        ).exclude(id__in=processed_item_ids).delete()

        return question

    def create(self, validated_data):
        items_data = validated_data.pop('survey_question_items', [])
        survey_question = SurveyQuestion.objects.create(**validated_data)

        if items_data:
            self._proceed_items(survey_question, items_data, create=True)

        return survey_question

    def update(self, instance, validated_data):
        """Обновление вопроса и его элементов."""
        items_data = validated_data.pop('survey_question_items', [])

        instance.text = validated_data.get('text', instance.text)
        instance.order = validated_data.get('order', instance.order)
        instance.save()

        if items_data:
            self._proceed_items(instance, items_data)
        else:
            instance.survey_question_items.all().delete()

        instance.refresh_from_db()
        return instance
