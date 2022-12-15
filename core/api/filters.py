from rest_framework import filters
from django_filters import rest_framework as django_filters


SEARCH_BACKEND_FILTER = (
    django_filters.DjangoFilterBackend,
    filters.SearchFilter,
)
