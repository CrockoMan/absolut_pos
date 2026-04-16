from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Survey
from core.views.api.v1.base import BaseModelViewSet
from core.views.api.v1.serializers.survey import SurveySerializer


class SurveyViewSet(BaseModelViewSet):
    """Вью опросов."""

    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated]

    # def get_serializer_class(self):
    #     if self.action in ['update', ]:
    #         return ProductionOrderWriterSerializer
    #     return ProductionOrderReaderSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
