from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class BaseGenericAbstractModel(TimeStampedModel):
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)ss", verbose_name=_('added by'),
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)ss",
        verbose_name=_('content type')
    )
    object_id = models.PositiveIntegerField(verbose_name=_('object id'))
    content_object = GenericForeignKey()

    class Meta:
        abstract = True
