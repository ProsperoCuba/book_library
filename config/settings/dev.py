from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = INSTALLED_APPS + ["django_extensions"]

AUTH_PASSWORD_VALIDATORS = []

INTERNAL_IPS = ["127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
