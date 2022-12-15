import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_select2.forms import Select2Widget

from core.enums import StatusBookLoanOptions, CHOICES_BOOLEAN_FILTER
from core.models import Author, Book, BookLoan
from utils.filters import SearchFilter


class AuthorFilter(SearchFilter):

    class Meta:
        model = Author
        fields = ["search"]

    def search_filter(self, queryset, name, value):
        return queryset.filter(full_name__icontains=value)


class BookFilter(SearchFilter):
    availability = django_filters.ChoiceFilter(field_name="availability", label=_('Disponibilidad'),
                                               choices=CHOICES_BOOLEAN_FILTER, widget=Select2Widget())

    class Meta:
        model = Book
        fields = ["search", "availability"]

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
            | Q(summary__icontains=value)
        )


class BookLoanFilter(SearchFilter):
    status = django_filters.ChoiceFilter(field_name="status", label=_('Estado'),
                                         choices=StatusBookLoanOptions.choices, widget=Select2Widget())

    class Meta:
        model = BookLoan
        fields = ["search", "status"]

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(customer__first_name__icontains=value)
            | Q(customer__last_name__icontains=value)
            | Q(customer__email__icontains=value)
            | Q(customer__phone_number__icontains=value)
        )
