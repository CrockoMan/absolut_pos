from rest_framework import serializers

from core.models import Survey
from core.views.api.v1.serializers.base import BaseModelSerializer


class SurveySerializer(BaseModelSerializer):
    """Сериализатор опросов."""

    class Meta(BaseModelSerializer.Meta):
        model = Survey
        fields = (
            'id',
            'author',
            'name',
            'survey_date',
        )

    def validate(self, obj):
        user = self.context['request'].user
        author = obj.get('author')

        if author != user and not user.is_admin:
            raise serializers.ValidationError({'author': 'Изменение автора запрещено'})

        return obj
