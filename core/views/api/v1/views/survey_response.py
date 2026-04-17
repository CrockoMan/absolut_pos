from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Survey
from core.views.api.v1.serializers.survey_response import SubmitAnswerSerializer
from core.views.api.v1.serializers.survey_response import SurveyResponseSerializer
from core.views.api.v1.serializers.survey_response import SurveyOneQuestionSerializer


class SurveyResponseViewSet(viewsets.ModelViewSet):

    queryset = Survey.objects.all()
    serializer_class = SurveyResponseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'survey_id'
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        survey = self.get_object()
        user = request.user

        serializer = SurveyOneQuestionSerializer(
            data={},
            survey=survey,
            user=user
        )

        try:
            serializer.is_valid(raise_exception=True)
            response_data = serializer.to_representation(None)
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e) if hasattr(e, 'detail') else str(e)
            if "опрос пройден" in error_message.lower():
                return Response(
                    {'message': 'Опрос пройден, отвечены все вопросы'},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": error_message},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, *args, **kwargs):
        survey = self.get_object()
        user = request.user

        serializer = SubmitAnswerSerializer(
            data=request.data,
            survey=survey,
            user=user
        )
        serializer.is_valid(raise_exception=True)

        response = serializer.save()

        response_data = {
            'message': 'Ответ сохранен',
            'response_id': response.id,
            'survey_id': survey.id,
            'question_id': response.survey_question.id,
            'answer': {
                'text': response.text,
                'item_id': response.survey_question_item.id if response.survey_question_item else None,
            },
            'completed_at': response.completed_at,
            'response_duration': response.response_duration,
        }

        return Response(response_data, status=status.HTTP_200_OK)
