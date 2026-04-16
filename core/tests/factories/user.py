import factory

from core.choices.role import UserRoleChoices
from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.Sequence(lambda n: 'user{}@librarius.com'.format(n))
    password = 'secret'
    role = UserRoleChoices.ROLE_USER
    is_staff = False
    is_superuser = False
    is_active = True

    class Meta:
        model = User
        django_get_or_create = ('email',)
