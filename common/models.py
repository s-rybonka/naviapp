from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from common.utils import get_file_upload_path


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


class FileQuerySet(models.QuerySet):
    def delete(self):
        for obj in self.iterator():
            default_storage.delete(obj.file.name)
        return super().delete()


class BaseFileCleanableModel(TimeStampedModel):
    file = models.FileField(upload_to=get_file_upload_path)

    objects = FileQuerySet.as_manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        default_storage.delete(self.file.name)
        return super().delete(using, keep_parents)

    @property
    def upload_prefix(self):
        return self.__class__.__name__.lower()
