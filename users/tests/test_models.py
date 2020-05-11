import pytest

from users.models import User
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestUserManager:
    def test_create_user(self):
        proto_user = UserFactory.build()
        user = User.objects.create_user(
            email=proto_user.email, password=proto_user._password, first_name=proto_user.first_name,
            last_name=proto_user.last_name, username=proto_user.username,
        )

        assert User.objects.filter(email=proto_user.email).exists()
        assert user.email == proto_user.email
        assert user.first_name == proto_user.first_name
        assert user.last_name == proto_user.last_name
        assert user.username == proto_user.username
        assert user.check_password(proto_user._password)
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_active
        assert not user.is_verified

        with pytest.raises(ValueError, match='The given email must be set'):
            User.objects.create_user(
                email='', password=proto_user._password, first_name=proto_user.first_name,
                last_name=proto_user.last_name, username=proto_user.username
            )

        with pytest.raises(ValueError, match='The given username must be set'):
            User.objects.create_user(
                email=proto_user.email, password=proto_user._password, first_name=proto_user.first_name,
                last_name=proto_user.last_name, username=''
            )

    def test_create_superuser(self):
        proto_user = UserFactory.build()
        user = User.objects.create_superuser(
            email=proto_user.email, password=proto_user._password, first_name=proto_user.first_name,
            last_name=proto_user.last_name, username=proto_user.username
        )

        assert User.objects.filter(email=proto_user.email).exists()
        assert user.email == proto_user.email
        assert user.first_name == proto_user.first_name
        assert user.last_name == proto_user.last_name
        assert user.username == proto_user.username
        assert user.check_password(proto_user._password)
        assert user.is_staff
        assert user.is_superuser
        assert user.is_active
        assert user.is_verified

        with pytest.raises(ValueError, match='The given email must be set'):
            User.objects.create_superuser(
                email='', password=proto_user._password, first_name=proto_user.first_name,
                last_name=proto_user.last_name, username=proto_user.username
            )

        with pytest.raises(ValueError, match='The given username must be set'):
            User.objects.create_superuser(
                email=proto_user.email, password=proto_user._password, first_name=proto_user.first_name,
                last_name=proto_user.last_name, username=''
            )

        with pytest.raises(ValueError, match='Superuser must have is_staff=True.'):
            User.objects.create_superuser(
                email=proto_user.email, password=proto_user._password, first_name=proto_user.first_name,
                last_name=proto_user.last_name, is_staff=False, username=proto_user.username
            )

        with pytest.raises(ValueError, match='Superuser must have is_superuser=True.'):
            User.objects.create_superuser(
                email=proto_user.email, password=proto_user._password, first_name=proto_user.first_name,
                last_name=proto_user.last_name, is_superuser=False, username=proto_user.username
            )


class TestUser:
    def test_get_full_name(self, user):
        assert user.get_full_name() == f'{user.first_name} {user.last_name}'.strip()

    def test_get_short_name(self, user):
        assert user.get_short_name() == user.first_name


class TestUserQuerySet:

    def test_is_email_verified_annotation(self):
        verified_user = UserFactory()
        unverified_user = UserFactory(populate_email__is_email_verified=False)

        queryset = User.objects.all().annotate_is_email_verified()

        assert queryset.get(id=verified_user.id).is_email_verified
        assert not queryset.get(id=unverified_user.id).is_email_verified
