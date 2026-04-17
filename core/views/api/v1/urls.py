from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views.api.v1.views.survey import SurveyViewSet
from core.views.api.v1.views.survey_response import SurveyResponseViewSet

app_name = 'v1'

router = DefaultRouter()
router.register('surveys', SurveyViewSet, basename='survey')
router.register('surveys_response', SurveyResponseViewSet, basename='survey_response')


urlpatterns = [
    path('', include(router.urls)),
]
