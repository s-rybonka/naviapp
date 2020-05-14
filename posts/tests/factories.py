import factory
from factory import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from common.factories import GenericRelationFactory
from posts.models import Like
from posts.models import Post
from users.tests.factories import UserFactory


class PostFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f'Post title-{n}')
    status = FuzzyChoice(Post.STATUSES)
    file = factory.django.ImageField()
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('paragraph')

    class Meta:
        model = Post


class LikeFactory(GenericRelationFactory):
    added_by = factory.SubFactory(UserFactory)
    content_object = factory.SubFactory(PostFactory)

    class Meta:
        model = Like
