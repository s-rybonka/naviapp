from django.urls import include
from django.urls import path
from rest_auth import views as rest_auth_views
from rest_auth.registration.views import RegisterView

from users import views as users_views


register_urls = [
    path("resend-email/", users_views.ResendVerificationEmailView.as_view(), name="resend-email"),
    path("verify-email/", users_views.VerifyEmailView.as_view(), name="verify-email"),
    path("", RegisterView.as_view(), name="register"),
]

auth_urls = [
    path("login/", rest_auth_views.LoginView.as_view(),
         name="login"),
    path("logout/", rest_auth_views.LogoutView.as_view(),
         name="logout"),
    path("password/reset/", rest_auth_views.PasswordResetView.as_view(),
         name="password-reset"),
    path("password/reset/confirm/",
         rest_auth_views.PasswordResetConfirmView.as_view(),
         name="password-reset-confirm"),
    path("password/change/", rest_auth_views.PasswordChangeView.as_view(),
         name="password-change"),
    path("register/", include(register_urls)),
]

urlpatterns = [
    path("auth/", include((auth_urls, "auth"))),
]
