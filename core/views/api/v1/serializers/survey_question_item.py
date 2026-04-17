from rest_framework import serializers

from core.models import SurveyQuestionItem
from core.views.api.v1.serializers.common import SurveyQuestionBase


class SurveyQuestionItemSerializer(SurveyQuestionBase):
    """Сериализатор для вопросов."""
    id = serializers.IntegerField(required=False)

    class Meta(SurveyQuestionBase.Meta):
        model = SurveyQuestionItem
