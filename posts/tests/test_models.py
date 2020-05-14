import pytest

from posts.models import Post
from posts.tests import factories as posts_factories


pytestmark = pytest.mark.django_db


class TestPostQueryset:
    def test_published_method(self):
        posts_factories.PostFactory.create_batch(10, status=Post.STATUSES.published)
        assert Post.objects.published().count() == 10

    def test_archived_method(self):
        posts_factories.PostFactory.create_batch(10, status=Post.STATUSES.archived)
        assert Post.objects.archived().count() == 10
