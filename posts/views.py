from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from common.utils import get_default_schema_responses
from posts import models as posts_models
from posts import serializers as posts_serializers


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        responses=get_default_schema_responses({
            '200': posts_serializers.PostModelSerializer,
        }, exclude=['400', '401', '403']),
    )
)
@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        request_body=posts_serializers.PostModelSerializer,
        responses=get_default_schema_responses({
            '200': posts_serializers.PostModelSerializer,
        }),
    )
)
@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        responses=get_default_schema_responses({
            '200': posts_serializers.PostModelSerializer,
        }, exclude=['400', '401', '403']),
    )
)
@method_decorator(
    name='update',
    decorator=swagger_auto_schema(
        request_body=posts_serializers.PostModelSerializer,
        responses=get_default_schema_responses({
            '200': posts_serializers.PostModelSerializer,
        }),
    )
)
@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        request_body=posts_serializers.PostModelSerializer,
        responses=get_default_schema_responses({
            '200': posts_serializers.PostModelSerializer,
        }),
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        responses=get_default_schema_responses({
            '200': posts_serializers.PostModelSerializer,
        }),
    )
)
class PostGenericViewSet(ModelViewSet):
    queryset = posts_models.Post.objects.all()
    serializer_class = posts_serializers.PostModelSerializer
