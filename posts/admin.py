from django.contrib import admin
from posts import models as posts_models

admin.site.register(posts_models.Post)
admin.site.register(posts_models.Like)
