from django.contrib import admin

from core.admin import BaseAdmin
from core.admin.resources.survey import SurveyResource
from core.models import Survey
from core.models import SurveyQuestion


class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 0
    fields = ['text', 'order',]


@admin.register(Survey)
class SurveyAdmin(BaseAdmin):
    resource_class = SurveyResource
    search_fields = ['author', 'name',]
    list_display_links = ('name',)
    list_display = ('id', 'name', 'author', 'survey_date', 'questions_count_display')
    list_filter = ('survey_date', 'author', )
    inlines = [
        SurveyQuestionInline,
    ]

    def questions_count_display(self, obj):
        return obj.survey_questions.count()
    questions_count_display.short_description = 'Всего вопросов'
