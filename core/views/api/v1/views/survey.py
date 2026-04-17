from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Survey
from core.views.api.v1.base import BaseModelViewSet
from core.views.api.v1.serializers.survey import SurveySerializer


class SurveyViewSet(BaseModelViewSet):

    serializer_class = SurveySerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Survey.objects.all().prefetch_related(
            'survey_questions',
            'survey_questions__survey_question_items',
        )
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
