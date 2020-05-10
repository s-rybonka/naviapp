from allauth.account.models import EmailAddress
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class UserQuerySet(models.QuerySet):
    def annotate_is_email_verified(self):
        subquery = EmailAddress.objects.filter(
            email=models.OuterRef("email"),
            user_id=models.OuterRef("id"),
            verified=True,
        )
        return self.annotate(is_email_verified=models.Exists(subquery))


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model)

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_verified', True)
        return super().create_superuser(username, email, password, **extra_fields)
