import pytest
from allauth.account.models import EmailConfirmationHMAC
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from users.models import User
from users.tests.factories import USER_PASSWORD
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestRegistrationAPIViewSet:
    registration_url = reverse("api:users:auth:register")
    email_verification_url = reverse("api:users:auth:verify-email")

    def test_registration(self, api_client):
        proto_user = UserFactory.build()

        signup_payload = {
            "email": proto_user.email,
            "password1": proto_user._password,
            "password2": proto_user._password,
        }

        response = api_client.post(self.registration_url, data=signup_payload)

        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert User.objects.filter(email=proto_user.email).exists()

    def test_invalid_registration(self, api_client):
        proto_user = UserFactory.build()

        signup_payload = {
            "email": proto_user.email,
            "password1": proto_user._password,
            "password2": 'another_password',
        }

        response = api_client.post(self.registration_url, data=signup_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "The two password fields didn't match." in response.data["non_field_errors"]

        user = UserFactory()

        signup_payload = {
            "email": user.email,
            "password1": proto_user._password,
            "password2": proto_user._password,
        }

        response = api_client.post(self.registration_url, data=signup_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "A user is already registered with this e-mail address." in response.data['field_errors']["email"]


class TestVerifyEmailView:
    verify_email_url = reverse("api:users:auth:verify-email")

    def test_verify_email(self, api_client):
        user = UserFactory(populate_email__is_email_verified=False)
        email_confirmation = EmailConfirmationHMAC(user.emailaddress_set.get(email=user.email))
        assert not user.emailaddress_set.filter(email=user.email, verified=True).exists()

        payload = {"key": email_confirmation.key}

        response = api_client.post(self.verify_email_url, data=payload)

        assert response.status_code == status.HTTP_200_OK
        assert user.emailaddress_set.filter(email=user.email, verified=True).exists()


class TestResendVerificationEmailView:
    resend_email_url = reverse("api:users:auth:resend-email")

    def test_resend_verification_email(self, api_client, mailoutbox):
        user = UserFactory(populate_email__is_email_verified=False)
        assert len(mailoutbox) == 0

        response = api_client.post(self.resend_email_url, data={"email": user.email})

        assert response.status_code == status.HTTP_200_OK
        assert len(mailoutbox) == 1

    def test_invalid_resend_verification_email(self, api_client, mailoutbox):
        user = UserFactory(populate_email__if_create_email=False)

        response = api_client.post(self.resend_email_url, data={"email": user.email})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email is not registered." in response.data['field_errors']["email"]
        assert len(mailoutbox) == 0

        user = UserFactory(populate_email__is_email_verified=True)
        response = api_client.post(self.resend_email_url, data={"email": user.email})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email was already verified." in response.data['field_errors']["email"]
        assert len(mailoutbox) == 0


class TestLoginView:
    login_url = reverse("api:users:auth:login")

    def test_login_via_email(self, api_client):
        user = UserFactory()
        password = USER_PASSWORD

        login_payload = {"email": user.email, "password": password}

        response = api_client.post(self.login_url, data=login_payload)

        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.wsgi_request.user.is_authenticated

        data = response.data
        assert "key" in data.keys()
        assert data["key"]
        assert "user" in data.keys()
        assert data["user"]["id"] == user.id
        assert data["user"]["email"] == user.email

    def test_login_with_invalid_credentials(self, api_client):
        user = UserFactory()

        login_payload = {"username": user.username, "password": "invalid"}

        response = api_client.post(self.login_url, data=login_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not response.wsgi_request.user.is_authenticated

    def test_optional_email_confirmed_validation(self, api_client):
        user = UserFactory(populate_email__is_email_verified=False)
        password = USER_PASSWORD

        login_payload = {"email": user.email, "password": password}

        response = api_client.post(self.login_url, data=login_payload)

        assert response.status_code == status.HTTP_200_OK


class TestLogoutView:
    logout_url = reverse("api:users:auth:logout")

    def test_happy_path(self, api_client, user):
        api_client.force_authenticate(user)

        response = api_client.post(self.logout_url)

        assert response.status_code == status.HTTP_200_OK
        assert not response.wsgi_request.user.is_authenticated


class TestPasswordChangeView:
    password_change_url = reverse("api:users:auth:password-change")

    def test_view_permission(self, api_client):
        response = api_client.post(self.password_change_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_password_change(self, api_client):
        password = USER_PASSWORD
        new_password = "new_P@ssword11"
        user = UserFactory(password=password)
        api_client.force_authenticate(user)

        data = {
            "old_password": "random password",
            "new_password1": new_password,
            "new_password2": new_password,
        }

        response = api_client.post(self.password_change_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data["old_password"] = password

        response = api_client.post(self.password_change_url, data=data)
        assert response.status_code == status.HTTP_200_OK

        assert user.check_password(new_password)


class TestPasswordResetView:
    password_reset_url = reverse("api:users:auth:password-reset")
    password_reset_confirm_url = reverse("api:users:auth:password-reset-confirm")

    def test_password_reset(self, api_client, user, mailoutbox):
        assert len(mailoutbox) == 0

        data = {
            "email": "not.existing@email.com"
        }
        response = api_client.post(self.password_reset_url, data=data)
        assert response.status_code == status.HTTP_200_OK, response.data
        assert len(mailoutbox) == 0

        data = {
            "email": user.email
        }

        response = api_client.post(self.password_reset_url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert len(mailoutbox) == 1

    def test_confirm_reset_email(self, api_client, user, mailoutbox):
        # send reset email
        new_password = "new_P@ssword11"
        api_client.post(self.password_reset_url, data={"email": user.email})

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        data = {
            "token": token,
            "uid": uid,
            "new_password1": new_password,
            "new_password2": new_password,
        }

        response = api_client.post(self.password_reset_confirm_url, data=data)
        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data["detail"] == "Password has been reset with the new password."

        user.refresh_from_db()
        assert user.check_password(new_password)

    def test_confirm_reset_email_validation(self, api_client, user, mailoutbox):
        # send reset email
        new_password = "new_P@ssword11"
        api_client.post(self.password_reset_url, data={"email": user.email})

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        data = {
            "token": "invalid_token",
            "uid": uid,
            "new_password1": new_password,
            "new_password2": new_password,
        }

        response = api_client.post(self.password_reset_confirm_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "token" in response.data['field_errors']

        data = {
            "token": token,
            "uid": "invalid_uid",
            "new_password1": new_password,
            "new_password2": new_password,
        }

        response = api_client.post(self.password_reset_confirm_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "uid" in response.data['field_errors']

        data = {
            "token": token,
            "uid": "invalid_uid",
            "new_password1": "password_mismatch",
            "new_password2": new_password,
        }

        response = api_client.post(self.password_reset_confirm_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "uid" in response.data['field_errors']
