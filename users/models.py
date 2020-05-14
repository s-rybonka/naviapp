from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.managers import UserManager


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(_('is verified by admin'), default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'User: {self.email}'
