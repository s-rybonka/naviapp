from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponseRedirect


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def get_email_confirmation_url(self, request, emailconfirmation):
        args = f"key={emailconfirmation.key}"
        return f"{settings.DJANGO_FRONTEND_PASSWORD_RESET_URL}{args}"

    def respond_email_verification_sent(self, request, user):
        return HttpResponseRedirect('/')
