# -*- coding: utf-8 -*-

import environ

from corsheaders.defaults import default_headers


ROOT_DIR = environ.Path(__file__) - 2

# Environment
# https://django-environ.readthedocs.io/en/latest/#how-to-use
# ------------------------------------------------------------------------------
# Default values and casting
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, ''),
    DJANGO_ADMINS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, []),
    # Static/Media
    DJANGO_STATIC_ROOT=(str, str(ROOT_DIR('staticfiles'))),
    DJANGO_MEDIA_ROOT=(str, str(ROOT_DIR('media'))),
    # Database
    POSTGRES_HOST=(str, 'db'),
    POSTGRES_PORT=(int, 5432),
    POSTGRES_DB=(str, ''),
    POSTGRES_USER=(str, ''),
    POSTGRES_PASSWORD=(str, ''),
    # Email
    DJANGO_EMAIL_URL=(environ.Env.email_url_config, 'consolemail://'),
    DJANGO_EMAIL_BACKEND=(str, 'django.core.mail.backends.smtp.EmailBackend'),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'admin@example.com'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost.com'),
    # Debug
    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    # Custom
    DJANGO_FRONTEND_PASSWORD_RESET_URL=(str, 'http://naviapp.com'),
    # Third party API
    # Cors
    DJANGO_CORS_ORIGIN_WHITELIST=(list, []),
    DJANGO_CORS_ALLOW_HEADERS=(tuple, ()),
    DJANGO_CORS_ORIGIN_ALLOW_ALL=(bool, False),
    # ImageKit
    DJANGO_IMAGEKIT_DEFAULT_FILE_STORAGE=(str, 'django.core.files.storage.FileSystemStorage'),
    # Api docs
    API_DOC_SCHEMA_TITLE=(str, 'NaviApp Rest API'),
    API_DOC_SCHEMA_DESCRIPTION=(str, 'Based on OpenAPI 2.0 Specification'),
    API_DOC_SCHEMA_AUTHOR_EMAIL=(str, 'developer@naviapp.com'),
)

# Django Core
# https://docs.djangoproject.com/en/2.2/ref/settings/#core-settings
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG")
SECRET_KEY = env('DJANGO_SECRET_KEY')
ROOT_URLCONF = 'naviapp.urls'
WSGI_APPLICATION = 'naviapp.wsgi.application'
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
ADMINS = tuple([
    tuple(admins.split(':'))
    for admins in env.list('DJANGO_ADMINS')
])
MANAGERS = ADMINS
ADMIN_URL = 'admin/'

TIME_ZONE = 'UTC'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Django Sites
# https://docs.djangoproject.com/en/2.2/ref/settings/#sites
# ------------------------------------------------------------------------------
SITE_ID = 1

# Django Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

# Django Applications
# https://docs.djangoproject.com/en/2.2/ref/settings/#installed-apps
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'allauth',
    'allauth.account',
    'corsheaders',
    'rest_auth',
    'rest_auth.registration',
    'imagekit',
    'rest_framework_tracking',
)
LOCAL_APPS = (
    'users.apps.UsersAppConfig',
    'posts.apps.PostsConfig',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Django Middlewares
# https://docs.djangoproject.com/en/2.2/ref/settings/#middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Django Email Server
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-backend
# ------------------------------------------------------------------------------
EMAIL_URL = env.email_url('DJANGO_EMAIL_URL')
EMAIL_BACKEND = EMAIL_URL['EMAIL_BACKEND']
EMAIL_HOST = EMAIL_URL.get('EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = EMAIL_URL.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = EMAIL_URL.get('EMAIL_HOST_USER', '')
EMAIL_PORT = EMAIL_URL.get('EMAIL_PORT', '')
EMAIL_USE_SSL = 'EMAIL_USE_SSL' in EMAIL_URL
EMAIL_USE_TLS = 'EMAIL_USE_TLS' in EMAIL_URL
EMAIL_FILE_PATH = EMAIL_URL.get('EMAIL_FILE_PATH', '')
EMAIL_SUBJECT_PREFIX = ''
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL')

# Django Templates
# https://docs.djangoproject.com/en/2.2/ref/settings/#templates
# ------------------------------------------------------------------------------
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        str(ROOT_DIR.path('templates')),
    ],
    'OPTIONS': {
        'debug': DEBUG,
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# Django Logging
# https://docs.djangoproject.com/en/2.2/ref/settings/#logging
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# Django Static Files
# https://docs.djangoproject.com/en/2.2/ref/settings/#static-files
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_ROOT')
STATICFILES_DIRS = (
    str(ROOT_DIR.path('static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Django Media Files
# https://docs.djangoproject.com/en/2.2/ref/settings/#media-root
# ------------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')

# Django Auth
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'api:users:auth:login'
LOGIN_REDIRECT_URL = '/'

# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_EMAIL_FIELD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGOUT_ON_GET = False

# django-rest-auth
# https://django-rest-auth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
LOGOUT_ON_PASSWORD_CHANGE = False
OLD_PASSWORD_FIELD_ENABLED = True
REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'users.serializers.LoginSerializer',
    'TOKEN_SERIALIZER': 'users.serializers.TokenSerializer',
    'PASSWORD_RESET_SERIALIZER': 'users.serializers.PasswordResetSerializer'
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.RegisterSerializer',
}

# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/
# ------------------------------------------------------------------------------
PAGE_SIZE = 20
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': PAGE_SIZE,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'common.exceptions.default_exception_handler',
}
# Django Debug Toolbar
# ------------------------------------------------------------------------------
USE_DEBUG_TOOLBAR = env.bool('DJANGO_USE_DEBUG_TOOLBAR')
if USE_DEBUG_TOOLBAR:
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', '10.0.2.2')
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

# Django CORS
# https://github.com/adamchainz/django-cors-headers#configuration
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = env.bool('DJANGO_CORS_ORIGIN_ALLOW_ALL')
CORS_ORIGIN_WHITELIST = env.list('DJANGO_CORS_ORIGIN_WHITELIST')
CORS_ALLOW_HEADERS = default_headers + env.tuple('DJANGO_CORS_ALLOW_HEADERS')

# Imagekit settings
# https://github.com/matthewwithanm/django-imagekit
# ------------------------------------------------------------------------------
DEFAULT_IMAGE_SIZE = (800, 800)
DEFAULT_IMAGE_QUALITY = 80
DEFAULT_IMAGE_EXTENSION = "JPEG"
IMAGEKIT_DEFAULT_FILE_STORAGE = env('DJANGO_IMAGEKIT_DEFAULT_FILE_STORAGE')
IMAGEKIT_CACHEFILE_DIR = ''

# Custom settings
# ------------------------------------------------------------------------------
DJANGO_FRONTEND_PASSWORD_RESET_URL = env('DJANGO_FRONTEND_PASSWORD_RESET_URL')

# Drf-yasg settings
# https://drf-yasg.readthedocs.io/en/stable/settings.html#swagger-settings
# ------------------------------------------------------------------------------
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'OPERATIONS_SORTER': 'alpha',
}

# API docs settings
# ------------------------------------------------------------------------------
API_DOC_SCHEMA_TITLE = env('API_DOC_SCHEMA_TITLE')
API_DOC_SCHEMA_DESCRIPTION = env('API_DOC_SCHEMA_DESCRIPTION')
API_DOC_SCHEMA_AUTHOR_EMAIL = env('API_DOC_SCHEMA_AUTHOR_EMAIL')
