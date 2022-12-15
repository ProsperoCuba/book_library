# from django.core.mail.backends.smtp import EmailBackend
# import threading
#
# from django.conf import settings
#
#
# class GmailBackend(EmailBackend):
#     """
#     A wrapper that manages the SMTP network connection.
#     """
#     def __init__(self, fail_silently=False, ssl_keyfile=None, ssl_certfile=None, **kwargs):
#         super().__init__(fail_silently=fail_silently)
#         self.host = constance_config.EMAIL_HOST
#         self.port = constance_config.EMAIL_PORT
#         self.username = constance_config.EMAIL_HOST_USER
#         self.password = constance_config.EMAIL_HOST_PASSWORD
#         self.use_tls = constance_config.EMAIL_USE_TLS
#         self.use_ssl = constance_config.EMAIL_USE_SSL
#         self.timeout = kwargs.get("timeout", None)
#         self.ssl_keyfile = settings.EMAIL_SSL_KEYFILE if ssl_keyfile is None else ssl_keyfile
#         self.ssl_certfile = settings.EMAIL_SSL_CERTFILE if ssl_certfile is None else ssl_certfile
#         if self.use_ssl and self.use_tls:
#             raise ValueError(
#                 "EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive, so only set "
#                 "one of those settings to True.")
#         self.connection = None
#         self._lock = threading.RLock()
