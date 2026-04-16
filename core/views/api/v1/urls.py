from django.urls import include
from django.urls import path
# from rest_framework.routers import SimpleRouter
from rest_framework.routers import DefaultRouter

from core.views.api.v1.views.survey import SurveyViewSet

app_name = 'v1'

# router = SimpleRouter()
router = DefaultRouter()
router.register('surveys', SurveyViewSet, basename='survey')


urlpatterns = [
    path('', include(router.urls)),
]
