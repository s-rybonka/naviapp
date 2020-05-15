from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


MANDATORY_ATTRIBUTE_HELP_TEXT = 'Mandatory response attribute.'
OPTIONAL_ATTRIBUTE_HELP_TEXT = 'Optional response attribute.'


class BaseErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        label=_('detail'), read_only=True, help_text=MANDATORY_ATTRIBUTE_HELP_TEXT,
    )


class FieldErrorSerializer(serializers.Serializer):
    field_key1 = serializers.ListField(serializers.CharField(
        label=_('field key 1')),
        help_text=OPTIONAL_ATTRIBUTE_HELP_TEXT
    )
    field_key2 = serializers.ListField(
        serializers.CharField(label=_('field key 1')),
        help_text=OPTIONAL_ATTRIBUTE_HELP_TEXT
    )


class ValidationErrorSerializer(serializers.Serializer):
    field_errors = FieldErrorSerializer(read_only=True, help_text='Sample keys.')
    non_field_errors = serializers.ListField(
        serializers.CharField(label=_('non field errors')), read_only=True,
        help_text=OPTIONAL_ATTRIBUTE_HELP_TEXT,
    )
    detail = serializers.CharField(
        label=_('detail'), read_only=True, help_text=OPTIONAL_ATTRIBUTE_HELP_TEXT,
    )


class AuthenticationErrorSerializer(BaseErrorSerializer):
    ...


class PermissionDeniedErrorSerializer(BaseErrorSerializer):
    ...


class NotFoundErrorSerializer(BaseErrorSerializer):
    ...


class MethodNotAllowedErrorSerializer(BaseErrorSerializer):
    ...


class OperationSerializer(serializers.Serializer):
    detail = serializers.CharField(label=_('detail'), read_only=True)


class PaginatedListSerializer(serializers.Serializer):
    count = serializers.IntegerField(read_only=True, label=_('count'))
    next = serializers.URLField(read_only=True, allow_null=True, label=_('next'))
    previous = serializers.URLField(read_only=True, allow_null=True, label=_('previous'))
    results = serializers.ListField(read_only=True, label=_('results'))

    class Meta:
        SWAGGER_REF_MODEL_NAME = 'PaginatedLisObject'
        ref_name = SWAGGER_REF_MODEL_NAME

    def __init__(self, *args, **kwargs):
        self.result_serializer = kwargs.pop('result_serializer', None)
        super().__init__(*args, **kwargs)
        self.fields['results'] = self.result_serializer(many=True, read_only=True)
