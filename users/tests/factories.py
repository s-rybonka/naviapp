from allauth.account.models import EmailAddress
from factory import DjangoModelFactory
from factory import Faker
from factory import PostGenerationMethodCall
from factory import post_generation


USER_PASSWORD = 'Password1'


class UserFactory(DjangoModelFactory):
    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    password = PostGenerationMethodCall('set_password', USER_PASSWORD)

    class Meta:
        model = 'users.User'
        django_get_or_create = ('email',)

    @post_generation
    def populate_email(self, create, extracted, **kwargs):
        if not create:
            return

        if kwargs.get("if_create_email", True):
            EmailAddress.objects.create(user=self, email=self.email, verified=kwargs.get("is_email_verified", True))
