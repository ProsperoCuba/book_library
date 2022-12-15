from rest_framework.routers import DefaultRouter

from .views import SelectLanguageViewSet, ServerTimeViewSet

router = DefaultRouter()
router.register("language", SelectLanguageViewSet, basename="language")
router.register("server-time", ServerTimeViewSet, basename="server_time")

urlpatterns = [
    # path("other-view", OtherViewViewSet.as_view(), name="other_view"),
] + router.urls
