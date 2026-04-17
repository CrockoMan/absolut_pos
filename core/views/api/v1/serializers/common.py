from core.models import SurveyQuestion
from core.views.api.v1.serializers.base import BaseModelSerializer


class SurveyQuestionBase(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        fields = (
            'id',
            'text',
            'order',
        )
