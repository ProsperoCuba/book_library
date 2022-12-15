from django.db.models import Q

from utils.filters import SearchFilter
from customers.models import Customer


class CustomerFilter(SearchFilter):

    class Meta:
        model = Customer
        fields = ["search"]

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(document_number__icontains=value)
            | Q(email__icontains=value)
            | Q(phone_number__icontains=value)
        )
