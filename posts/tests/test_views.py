import pytest
from django.urls import reverse
from rest_framework import status

from posts.models import Post
from posts.tests import factories as posts_factories


pytestmark = pytest.mark.django_db


class TestPostGenericViewSet:
    posts_list_url = reverse('api:posts:posts-list')
    post_detail_url = 'api:posts:posts-detail'

    def test_list_action(self, api_client):
        posts = reversed(posts_factories.PostFactory.create_batch(10, status=Post.STATUSES.published))

        response = api_client.get(self.posts_list_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 10

        for post_origin, post_response in zip(posts, response.data['results']):
            assert post_origin.id == post_response['id']
            assert post_origin.author.id == post_response['author']['id']
            assert post_origin.title == post_response['title']
            assert post_origin.content == post_response['content']

    def test_retrieve_action(self, api_client):
        post = posts_factories.PostFactory(status=Post.STATUSES.published)
        response = api_client.get(reverse(self.post_detail_url, args=(post.id,)))

        assert response.status_code == status.HTTP_200_OK

        assert post.id == response.data['id']
        assert post.author.id == response.data['author']['id']
        assert post.title == response.data['title']
        assert post.content == response.data['content']

    def test_create_action(self, api_client, user):
        api_client.force_authenticate(user)

        post = posts_factories.PostFactory.build()

        payload = {
            'title': post.title,
            'author': user.id,
            'content': post.content,
        }

        response = api_client.post(self.posts_list_url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert payload['title'] == response.data['title']
        assert payload['author'] == response.data['author']['id']
        assert payload['content'] == response.data['content']

    def test_delete_action(self, api_client, user):
        api_client.force_authenticate(user)
        post = posts_factories.PostFactory(status=Post.STATUSES.published)
        response = api_client.delete(reverse(self.post_detail_url, args=(post.id,)))

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestLikeGenericViewSet:
    like_list_url = reverse('api:posts:likes-list')
    like_detail_url = 'api:posts:likes-detail'
    like_analytic_url = reverse('api:posts:likes-analytics')

    def test_action_create(self, api_client, user):
        api_client.force_authenticate(user)

        post = posts_factories.PostFactory()

        payload = {
            'added_by': user.id,
            'content_object': post.id,
        }

        response = api_client.post(self.like_list_url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert payload['added_by'] == response.data['added_by']
        assert payload['content_object'] == response.data['content_object']

    def test_delete_action(self, api_client, user):
        api_client.force_authenticate(user)

        like = posts_factories.LikeFactory()
        response = api_client.delete(reverse(self.like_detail_url, args=(like.id,)))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_analytics_action(self, api_client, user):
        posts_factories.LikeFactory.create_batch(10)

        response = api_client.get(self.like_analytic_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['date'] is not None
        assert response.data[0]['likes_count'] == 10
