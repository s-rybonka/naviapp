import os
import uuid

from django.utils import timezone
from drf_yasg import openapi
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from common import serializers as common_serializers


def get_default_schema_responses(success_response, exclude=None):
    responses = {
        '400': openapi.Response(
            'Bad request. DRF API Exception classes: ValidationError, ParseError.',
            schema=common_serializers.ValidationErrorSerializer,
        ),
        '401': openapi.Response(
            'Unauthorized. Invalid token. DRF API Exception classes: AuthenticationFailed, NotAuthenticated.',
            schema=common_serializers.AuthenticationErrorSerializer,
        ),
        '403': openapi.Response(
            'Permission denied. DRF API Exception class: PermissionDenied.',
            schema=common_serializers.PermissionDeniedErrorSerializer,
        ),
        '404': openapi.Response(
            'Not found. DRF API Exception class: NotFound.',
            schema=common_serializers.NotFoundErrorSerializer,
        ),
        '405': openapi.Response(
            'Method not allowed. DRF API Exception class: MethodNotAllowed.',
            schema=common_serializers.MethodNotAllowedErrorSerializer,
        ),
    }
    responses = responses.copy()
    responses.update(success_response)

    if exclude:
        for response_to_exclude in exclude:
            responses.pop(response_to_exclude)

    return responses


class NotFoundAPIHandler(APIView):

    def get(self, request, *args, **kwargs):
        raise NotFound


drf_handler404 = NotFoundAPIHandler.as_view()


def get_file_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)

    return '{0}/{1}/{2}{3}'.format(
        instance.upload_prefix,
        timezone.now().strftime('%y/%m'),
        uuid.uuid4().hex,
        ext.lower())
