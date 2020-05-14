from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from posts import models as posts_models
from users.serializers import UserShortSerializer


class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts_models.Post
        fields = ('id', 'title', 'author', 'file', 'content', 'created', 'modified')
        read_only_fields = ('author',)
        SWAGGER_REF_MODEL_NAME = 'PostObject'
        ref_name = SWAGGER_REF_MODEL_NAME

    def to_representation(self, instance):
        post = super().to_representation(instance)
        post['author'] = UserShortSerializer(instance.author).data
        return post


class LikeModelSerializer(serializers.ModelSerializer):
    content_object = serializers.PrimaryKeyRelatedField(
        label=_('content object'),
        queryset=posts_models.Post.objects.all(),
    )

    class Meta:
        model = posts_models.Like
        fields = ('id', 'added_by', 'content_object')
        read_only_fields = ('added_by',)
        SWAGGER_REF_MODEL_NAME = 'LikeObject'
        ref_name = SWAGGER_REF_MODEL_NAME

    def validate(self, attrs):
        request = self.context.get('request')
        content_object = attrs.get('content_object')
        like_qs = posts_models.Like.objects.filter(
            added_by=request.user, object_id=content_object.id,
        )
        if like_qs.exists():
            raise serializers.ValidationError({
                'content_object': _('Post already liked.')
            })
        return attrs


class LikeGroupByDateSerializer(serializers.Serializer):
    date = serializers.DateTimeField(read_only=True, label=_('date'))
    likes_count = serializers.IntegerField(read_only=True, label=_('likes count'))

    class Meta:
        SWAGGER_REF_MODEL_NAME = 'LikeGroupByDateObject'
        ref_name = SWAGGER_REF_MODEL_NAME
