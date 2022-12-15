from django.utils.translation import gettext_lazy as _
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

urlpatterns = [
    path("docs/", include_docs_urls(title=str(_("Librería")), public=False,
                                            permission_classes=(AllowAny,),
                                            schema_url='/')),
    path('i18n/', include('django.conf.urls.i18n')),

    # Apps
    path('core/', include("core.api.urls")),
]
