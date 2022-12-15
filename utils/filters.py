import django_filters
from django.utils.translation import gettext_lazy as _


class SearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label=_("Search"), method="search_filter")

    class Meta:
        fields = ("search",)

    def search_filter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })
