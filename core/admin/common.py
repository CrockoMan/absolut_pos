from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from import_export.formats import base_formats

from core.models import User


class BaseAdmin(ExportActionModelAdmin):
    readonly_fields = ()
    formats = [base_formats.CSV, base_formats.XLSX]
    list_per_page = 20


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
