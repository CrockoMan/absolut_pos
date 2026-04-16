from django.utils.translation import gettext_lazy as _
from djchoices import ChoiceItem
from djchoices import DjangoChoices


class UserRoleChoices(DjangoChoices):
    ROLE_USER = ChoiceItem('SIMPLE_USER', _('Пользователь'))
    ROLE_SURVEY_ADMIN = ChoiceItem('SURVEY_ADMIN', _('Администратор'))
