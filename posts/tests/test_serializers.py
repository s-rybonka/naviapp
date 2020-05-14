import pytest

from posts import serializers as posts_serializers
from posts.tests import factories as posts_factories


pytestmark = pytest.mark.django_db


class TestPostModelSerializer:

    def test_to_representation(self):
        post = posts_factories.PostFactory()

        serializer = posts_serializers.PostModelSerializer(
            instance=post,
        )
        assert post.id == serializer.data['id']
        assert post.author.id == serializer.data['author']['id']
        assert post.title == serializer.data['title']
        assert post.content == serializer.data['content']


class TestLikeModelSerializer:

    def test_to_representation(self):
        like = posts_factories.LikeFactory()

        serializer = posts_serializers.LikeModelSerializer(
            instance=like,
        )
        assert like.id == serializer.data['id']
        assert like.added_by.id == serializer.data['added_by']
        assert like.content_object.id == serializer.data['content_object']
