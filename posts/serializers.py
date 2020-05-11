from rest_framework import serializers

from posts import models as posts_models
from users.serializers import UserShortSerializer


class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts_models.Post
        fields = ('author', 'title', 'content', 'created', 'modified')

    def to_representation(self, instance):
        post = super().to_representation(instance)
        post['author'] = UserShortSerializer(instance.author)
        return post


class LikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = posts_models.Like
        fields = ('id', 'added_by')
