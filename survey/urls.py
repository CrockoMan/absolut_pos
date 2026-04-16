from django.contrib import admin
from django.urls import include
from django.urls import path

from core import urls as core_urls

app_name = 'core'

urlpatterns = [
    path('', include((core_urls, app_name), namespace='core')),
    path('admin/', admin.site.urls),
]
