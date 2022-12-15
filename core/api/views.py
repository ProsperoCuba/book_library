from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .filters import SEARCH_BACKEND_FILTER
from .serializers import BookSerializer


# ViewSet for the model Book
from ..models import Book


class BookViewSet(mixins.ListModelMixin, GenericViewSet):
    """ViewSet to model Book"""
    serializer_class = BookSerializer
    queryset = Book.objects.filter(in_stock__gt=0)
    permission_classes = (DjangoModelPermissions,)
    filter_backends = SEARCH_BACKEND_FILTER
    search_fields = ["title", "author__full_name"]
