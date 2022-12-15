import os

from decouple import config
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="strong-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_filters",
    "django_tables2",
    "django_select2",
    "widget_tweaks",
    "rest_framework",

    # APPs
    "users.apps.UsersConfig",
    "core.apps.CoreConfig",
    "customers.apps.CustomersConfig",
    "utils.apps.UtilsConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "core.context_processors.global_variables",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": config("SQL_DATABASE", default=os.path.join(BASE_DIR, 'db.sqlite3')),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
gettext = lambda s: s
LANGUAGE_CODE = "es"
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
LANGUAGES = (("es", _("Spanish")), ("en", _("English")))

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles/")]
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# LOGIN options
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/admin/login/?next=/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/admin/login/?next=/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
        "rq.worker": {"handlers": ["console"], "level": "DEBUG"},
    },
}

MESSAGE_TAGS = {messages.ERROR: "danger"}
DJANGO_TABLES2_TEMPLATE = "tables2/bootstrap5.html"

DEFAULT_FROM_EMAIL = "library@gmail.com"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "utils.authentication.CsrfExemptSessionAuthentication",
        "rest_framework.authentication.SessionAuthentication",

    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework_datatables.renderers.DatatablesRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": ("rest_framework_datatables.filters.DatatablesFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.CustomDatatablesPageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ]
}
