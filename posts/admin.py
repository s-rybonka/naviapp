from django.contrib import admin

from posts import models as posts_models


@admin.register(posts_models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created')


@admin.register(posts_models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'added_by', 'created')
