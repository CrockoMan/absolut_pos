from django.urls import include
from django.urls import path
from core.views import urls as api_urls

app_name = 'core'

urlpatterns = [
    path('api/', include((api_urls, app_name), namespace='api')),
]
