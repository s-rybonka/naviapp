from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_auth import serializers as rest_auth_serializers
from rest_auth import views as rest_auth_views
from rest_auth.registration.views import RegisterView

from common.serializers import OperationSerializer
from common.utils import get_default_schema_responses
from users import serializers as users_serializers
from users import views as users_views


register_swg_auto_schema = swagger_auto_schema(
    method='post',
    request_body=users_serializers.RegisterSerializer,
    responses=get_default_schema_responses({
        '201': users_serializers.TokenSerializer
    }, exclude=['401']),
    operation_id='auth-register',
)

login_swg_auto_schema = swagger_auto_schema(
    method='post',
    responses=get_default_schema_responses({
        '200': users_serializers.TokenSerializer,
    }, exclude=['401', '403']),
    operation_id='auth-login',
)

logout_swg_auto_schema = swagger_auto_schema(
    methods=['get', 'post'],
    responses=get_default_schema_responses({
        '200': openapi.Response(description='Successful logged out.'),
    }, exclude=['400', '401', '403']),
)

pwd_reset_swg_auto_schema = swagger_auto_schema(
    method='post',
    request_body=users_serializers.PasswordResetSerializer,
    responses=get_default_schema_responses({
        '200': openapi.Response(
            description='Operation successful.',
            schema=OperationSerializer,
        ),
    }, exclude=['401', '403']),
    operation_id='auth-password-reset',
)

pwd_reset_confirm_swg_auto_schema = swagger_auto_schema(
    method='post',
    request_body=rest_auth_serializers.PasswordResetConfirmSerializer,
    responses=get_default_schema_responses({
        '200': openapi.Response(
            description='Operation successful.',
            schema=OperationSerializer,
        ),
    }, exclude=['401', '403']),
    operation_id='auth-password-reset-confirm',
)

pwd_change_swg_auto_schema = swagger_auto_schema(
    method='post',
    request_body=rest_auth_serializers.PasswordChangeSerializer,
    responses=get_default_schema_responses({
        '200': openapi.Response(
            description='Operation successful.',
            schema=OperationSerializer,
        ),
    }),
    operation_id='auth-password-change',
)

register_urls = [
    path("", register_swg_auto_schema(RegisterView.as_view()), name="register"),
    path("resend-email/", users_views.ResendVerificationEmailView.as_view(), name="resend-email"),
    path("verify-email/", users_views.VerifyEmailView.as_view(), name="verify-email"),
]

auth_urls = [
    path("login/", login_swg_auto_schema(rest_auth_views.LoginView.as_view()),
         name="login"),
    path("logout/", logout_swg_auto_schema(rest_auth_views.LogoutView.as_view()),
         name="logout"),
    path("password/reset/", pwd_reset_swg_auto_schema(rest_auth_views.PasswordResetView.as_view()),
         name="password-reset"),
    path("password/reset/confirm/",
         pwd_reset_confirm_swg_auto_schema(rest_auth_views.PasswordResetConfirmView.as_view()),
         name="password-reset-confirm"),
    path("password/change/", pwd_change_swg_auto_schema(rest_auth_views.PasswordChangeView.as_view()),
         name="password-change"),
    path("register/", include(register_urls)),
]

urlpatterns = [
    path("auth/", include((auth_urls, "auth"))),
    path("profile-detail/", users_views.UserRetrieveAPIView.as_view(), name='profile-detail')
]
