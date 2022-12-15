import django_filters
from django.db.models import Q
from django.forms import DateInput
from django.utils.translation import gettext_lazy as _

from utils.filters import SearchFilter
from .models import User


class UserFilter(SearchFilter):
    date_joined = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), field_name='date_joined',
                                           lookup_expr="icontains", label=_("Fecha de alta"))

    username = django_filters.CharFilter(field_name='username', lookup_expr="icontains",
                                             label=User._meta.get_field("username").verbose_name)
    email = django_filters.CharFilter(field_name='email', lookup_expr="icontains",
                                             label=User._meta.get_field("email").verbose_name)
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr="icontains",
                                             label=User._meta.get_field("phone_number").verbose_name)

    class Meta:
        model = User
        fields = {
            "is_superuser": ["exact"],
            "is_active": ["exact"],
        }

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value)
            | Q(first_name__icontains=value)
            | Q(first_name__icontains=value)
            | Q(email__icontains=value)
            | Q(phone_number__icontains=value)
        )
