import factory
from factory import Faker

from core.choices.role import UserRoleChoices
from core.models import Survey
from core.tests.factories.user import UserFactory


class SurveyFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory(
        UserFactory,
        role=UserRoleChoices.ROLE_SURVEY_ADMIN
    )
    name = Faker('word')

    class Meta:
        model = Survey
