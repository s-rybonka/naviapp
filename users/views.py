from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_auth.registration.views import VerifyEmailView as BaseVerifyEmailView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from common.utils import get_default_schema_responses
from users import serializers as users_serializers
from users import models as users_models


class ResendVerificationEmailView(GenericAPIView):
    serializer_class = users_serializers.EmailVerificationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_email()
        return Response(data={"detail": _("Email was re-send")}, status=status.HTTP_200_OK)


class VerifyEmailView(BaseVerifyEmailView):
    """
    Explicit declaration of this view is a workaround.
    Because endpoint `/verify-email/` fails on GET method because of redundant
    declaration of allowed HTTP methods in `VerifyEmailView` via `attribute allowed_methods`.
    https://github.com/Tivix/django-rest-auth/issues/581
    """
    http_method_names = [verb.lower() for verb in BaseVerifyEmailView.allowed_methods]


@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        responses=get_default_schema_responses({
            '200': users_serializers.UserDetailSerializer,
        }, exclude=['400']),
        operation_id='profile-detail',
    )
)
class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = users_serializers.UserDetailSerializer
    queryset = users_models.User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user