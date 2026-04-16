from django.urls import include
from django.urls import path

from core.views.api.v1 import urls as api_v1_urls

app_name = 'api'


urlpatterns = [
    path('v1/', include((api_v1_urls, app_name), namespace='v1')),
]
