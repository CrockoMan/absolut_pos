from django.core.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.views.api.v1.pagination import CustomPageNumberPagination


class HandleModelValidationMixin:

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(self._format_validation_error(e))

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(self._format_validation_error(e))

    def _format_validation_error(self, error):
        """Форматирование ValidationError из модели в формат DRF"""
        if hasattr(error, 'message_dict'):
            return error.message_dict
        return {'non_field_errors': error.messages}


class BaseModelViewSet(HandleModelValidationMixin, ModelViewSet):
    pagination_class = CustomPageNumberPagination

    http_method_names = ['get', ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Номер страницы",
                type=openapi.TYPE_INTEGER,
                default=1
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Количество элементов на странице",
                type=openapi.TYPE_INTEGER,
                default=50
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            if hasattr(exc, 'message_dict'):
                return Response(exc.message_dict, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {'detail': str(exc) if exc else 'Ошибка валидации'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().handle_exception(exc)
