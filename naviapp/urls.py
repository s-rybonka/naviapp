from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from common.utils import drf_handler404


schema_view = get_schema_view(
    openapi.Info(
        title=settings.API_DOC_SCHEMA_TITLE,
        default_version='v1',
        description=settings.API_DOC_SCHEMA_DESCRIPTION,
        contact=openapi.Contact(email=settings.API_DOC_SCHEMA_AUTHOR_EMAIL),
    ),
    public=False,
)

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path('', lambda request: redirect('api:docs')),
    # API urls
    path('api/v1/', include(([
    path('', include(('users.urls', 'users'))),
    path('docs/', schema_view.with_ui(), name='docs'),
    ], 'api'), namespace='api')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = drf_handler404

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns