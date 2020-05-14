from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins as drf_mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework_tracking.mixins import LoggingMixin

from common.serializers import OperationSerializer
from common.serializers import PaginatedListSerializer
from common.utils import get_default_schema_responses
from posts import models as posts_models
from posts import serializers as posts_serializers
from posts.filters import LikeFilter


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        responses=get_default_schema_responses({
            '200': PaginatedListSerializer(
                result_serializer=posts_serializers.PostModelSerializer,
            ),
        }, exclude=['400', '401', '403']),
    )
)
@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        request_body=posts_serializers.PostModelSerializer,
        responses=get_default_schema_responses({
            '201': posts_serializers.PostModelSerializer,
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
            '204': OperationSerializer,
        }),
    )
)
class PostGenericViewSet(LoggingMixin, ModelViewSet):
    queryset = posts_models.Post.objects.published()
    serializer_class = posts_serializers.PostModelSerializer


@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        responses=get_default_schema_responses({
            '201': posts_serializers.LikeModelSerializer,
        }),
    )
)
@method_decorator(
    name='destroy',
    decorator=swagger_auto_schema(
        responses=get_default_schema_responses({
            '204': OperationSerializer,
        }, exclude=['400']),
    )
)
@method_decorator(
    name='analytics',
    decorator=swagger_auto_schema(
        responses=get_default_schema_responses({
            '200': posts_serializers.LikeGroupByDateSerializer(many=True),
        }, exclude=['400']),
    ),
)
class LikeGenericViewSet(
    LoggingMixin,
    drf_mixins.CreateModelMixin,
    drf_mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = posts_serializers.LikeModelSerializer
    queryset = posts_models.Like.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LikeFilter
    pagination_class = None
    analytic_serializer = posts_serializers.LikeGroupByDateSerializer

    @action(detail=False)
    def analytics(self, request):
        like_qs = self.filter_queryset(self.get_queryset())
        filtered_like_qs = like_qs.group_by_date()
        data = self.analytic_serializer(filtered_like_qs, many=True).data
        return Response(data)
