from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


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

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-id',)

    def __str__(self):
        return f'Post:{self.title}'
