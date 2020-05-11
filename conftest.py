import django
import pytest
from django.conf import settings as base_settings
from django.test import RequestFactory

from rest_framework.test import APIClient

from users.tests.factories import UserFactory


# def pytest_configure():
#     django.setup()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> base_settings.AUTH_USER_MODEL:
    return UserFactory(is_verified=True)


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
