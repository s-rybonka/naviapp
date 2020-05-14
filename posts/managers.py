from django.db.models import Count
from django.db.models import QuerySet
from django.db.models import functions as dj_db_functions

from posts import models as posts_models


class LikeQueryset(QuerySet):
    def group_by_date(self):
        return (self.annotate(date=dj_db_functions.TruncDay('created'))
                .values('date')
                .order_by('-date')
                .annotate(likes_count=Count('id')))


class PostQueryset(QuerySet):
    def published(self):
        return self.filter(status=posts_models.Post.STATUSES.published)

    def archived(self):
        return self.filter(status=posts_models.Post.STATUSES.archived)
