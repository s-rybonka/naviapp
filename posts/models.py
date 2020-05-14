from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel

from common.models import BaseGenericAbstractModel
from posts.managers import LikeQueryset


class Post(TimeStampedModel):
    STATUSES = Choices(
        ('published', _('Published')),
        ('archived', _('Archived')),
    )
    title = models.CharField(max_length=150, verbose_name=_('title'))
    status = StatusField(
        verbose_name=_('status'), choices_name='STATUSES',
        db_index=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name=_('author'), related_name='posts',
    )
    content = models.TextField(verbose_name=_('content'))
    likes = GenericRelation(
        'Like', related_query_name='post',
        verbose_name=_('likes'),
    )

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-id',)

    def __str__(self):
        return f'Post: {self.title}'

    @classmethod
    def get_content_type(cls):
        return ContentType.objects.get(
            app_label='posts',
            model=cls.__name__.lower(),
        )


class Like(BaseGenericAbstractModel):
    objects = LikeQueryset.as_manager()

    class Meta:
        verbose_name = _('like')
        verbose_name_plural = _('likes')
        ordering = ('-id',)

    def __str__(self):
        return f'Liked by: {self.added_by}'
