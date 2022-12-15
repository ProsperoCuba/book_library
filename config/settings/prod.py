from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

# used in production
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DATA_UPLOAD_MAX_MEMORY_SIZE = 200 * 1000000

EMAIL_BACKEND = "core.email_backend.GmailBackend"
