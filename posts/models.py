from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from pilkit.processors import Anchor
from pilkit.processors import ResizeToFit

from common.models import BaseFileCleanableModel
from common.models import BaseGenericAbstractModel
from common.utils import get_file_upload_path
from posts import managers as posts_managers


class Post(BaseFileCleanableModel):
    STATUSES = Choices(
        ('published', _('Published')),
        ('archived', _('Archived')),
    )
    title = models.CharField(max_length=150, verbose_name=_('title'))
    status = StatusField(
        verbose_name=_('status'), choices_name='STATUSES',
        db_index=True,
    )
    file = ProcessedImageField(
        upload_to=get_file_upload_path,
        processors=[ResizeToFit(*settings.DEFAULT_IMAGE_SIZE, anchor=Anchor.CENTER, upscale=False)],
        format=settings.DEFAULT_IMAGE_EXTENSION,
        options={'quality': settings.DEFAULT_IMAGE_QUALITY},
        verbose_name=_('image file'),
        null=True, blank=True,
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
    objects = posts_managers.PostQueryset.as_manager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-id',)

    def __str__(self):
        return f'Post: {self.title}'


class Like(BaseGenericAbstractModel):
    objects = posts_managers.LikeQueryset.as_manager()

    class Meta:
        verbose_name = _('like')
        verbose_name_plural = _('likes')
        ordering = ('-id',)

    def __str__(self):
        return f'Liked by: {self.added_by}'
