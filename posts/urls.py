from django.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter

from posts import views as posts_views


router = SimpleRouter()
router.register('posts', posts_views.PostGenericViewSet, 'posts')
router.register('likes', posts_views.LikeGenericViewSet, 'likes')

urlpatterns = [
    path('', include(router.urls))
]
