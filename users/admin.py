from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from users.forms import UserChangeForm
from users.forms import UserCreationForm
from users.models import User


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 0


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('id', 'email', 'username', 'password', 'token')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined', 'id', 'token')

    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'date_joined', 'last_login',
        'is_verified', 'is_email_verified'
    )
    list_display_links = ('email',)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    inlines = [EmailAddressInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate_is_email_verified()

    def is_email_verified(self, user):
        return user.is_email_verified

    is_email_verified.boolean = True

    @staticmethod
    def token(user):
        return user.auth_token.key

    def get_list_filter(self, request):
        return super().get_list_filter(request) + ('is_verified',)
