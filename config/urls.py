from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

admin.site.site_header = _("Administración de Librería")
admin.site.site_title = _("Portal Admin de Librería")
admin.site.index_title = _("Bienvenido al Portal Admin de Librería")

urlpatterns = [
    path("", RedirectView.as_view(url="dashboard/", permanent=False), name="home"),
    path("select2/", include("django_select2.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path('api/v1/', include("api.urls")),
    path("dashboard/users/", include("users.urls")),
    path("dashboard/logout/", logout_then_login, name="logout"),
    path("dashboard/utils/", include("utils.urls")),
    path("dashboard/", include("core.urls")),
    path("dashboard/customer", include("customers.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
