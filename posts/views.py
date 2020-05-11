from rest_framework.viewsets import ModelViewSet

from posts import models as posts_models
from posts import serializers as posts_serializers


class PostGenericViewSet(ModelViewSet):
    queryset = posts_models.Post.objects.all()
    serializer_class = posts_serializers.PostModelSerializer
