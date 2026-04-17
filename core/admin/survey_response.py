from django.contrib import admin

from core.models import SurveyResponse


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_survey_name', 'user', 'started_at', 'completed_at']
    list_filter = ['survey_question__survey__name']
    search_fields = ['user__email', 'text', 'survey_question__text']

    def get_survey_name(self, obj):
        return obj.survey_question.survey.name if obj.survey_question.survey else '-'

    get_survey_name.short_description = 'Опрос'
    get_survey_name.admin_order_field = 'survey_question__survey__name'
