from rest_framework.routers import DefaultRouter

from .views import BookViewSet

router = DefaultRouter()

# Endpoints for the module Book
router.register("books", BookViewSet, basename="books")

urlpatterns = [] + router.urls
