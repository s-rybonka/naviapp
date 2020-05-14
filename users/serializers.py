from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from django.conf import settings
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_serializer_method
from rest_auth.models import TokenModel
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from rest_auth.serializers import PasswordResetSerializer as BasePasswordResetSerializer
from rest_auth.serializers import TokenSerializer as BaseTokenSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, help_text=_('Email address'))
    password1 = serializers.CharField(write_only=True, help_text=_('Password'))
    password2 = serializers.CharField(write_only=True, help_text=_('Password Confirmation'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_data = {}

    @staticmethod
    def validate_email(email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(_("A user is already registered with this e-mail address."))
        return email

    @staticmethod
    def validate_password1(password):
        return get_adapter().clean_password(password)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return attrs

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class LoginSerializer(RestAuthLoginSerializer):
    username = None
    email = serializers.EmailField(label=_('email'))


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = EmailAddress
        fields = ("email",)

    @staticmethod
    def validate_email(value):
        try:
            email = EmailAddress.objects.get(email=value)
        except EmailAddress.DoesNotExist:
            raise ValidationError(_("Email is not registered."))
        else:
            if email.verified:
                raise ValidationError(_("Email was already verified."))
        return value

    def send_email(self):
        obj = EmailAddress.objects.get(email=self.validated_data["email"])
        obj.send_confirmation()


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username")
        read_only_fields = fields


class TokenSerializer(BaseTokenSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = TokenModel
        fields = ("key", "user")
        read_only_fields = fields


class PasswordResetSerializer(BasePasswordResetSerializer):

    def get_email_options(self):
        return {
            "extra_email_context": {
                "password_reset_url": settings.DJANGO_FRONTEND_PASSWORD_RESET_URL
            }
        }


class UserDetailSerializer(serializers.ModelSerializer):
    last_activity = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "username", "last_login", "last_activity")
        read_only_fields = fields
        SWAGGER_REF_MODEL_NAME = 'UserDetailObject'
        ref_name = SWAGGER_REF_MODEL_NAME

    @staticmethod
    @swagger_serializer_method(serializer_or_field=serializers.DateTimeField)
    def get_last_activity(user):
        request_log_last_request = getattr(
            user.apirequestlog_set.last(),
            'requested_at', '',
        )
        return request_log_last_request
