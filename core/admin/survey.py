from django.contrib import admin

from core.models import Survey
from core.models import SurveyQuestion


class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestion
    extra = 0
    fields = ['text', 'order',]


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    search_fields = ['author', 'name',]
    list_display_links = ('name',)
    list_display = ('id', 'name', 'author', 'survey_date')
    list_filter = ('survey_date', 'author', )
    inlines = [
        SurveyQuestionInline,
    ]
