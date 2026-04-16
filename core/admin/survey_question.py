from django.contrib import admin

from core.models import SurveyQuestion
from core.models import SurveyQuestionItem


class SurveyQuestionInline(admin.TabularInline):
    model = SurveyQuestionItem
    extra = 0
    fields = ['text', 'order',]


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    search_fields = ['survey', 'text',]
    list_display = ('id', 'survey', 'text', 'order')
    list_filter = ('survey',  )
    inlines = [
        SurveyQuestionInline,
    ]
