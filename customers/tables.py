import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from customers.models import Customer


class CustomerTable(tables.Table):
    actions = tables.columns.TemplateColumn(
        verbose_name=_("Acciones"),
        template_name="customers/actions.html",
        orderable=False,
    )
    full_name = tables.columns.TemplateColumn(verbose_name=_("Nombre"), template_name="customers/full_name.html",
                                              orderable=False)
    document_number = tables.Column(verbose_name=_("DNI/NIE/Pasaporte"), accessor="document_number")
    email = tables.Column(verbose_name=_("Email"), accessor="email")
    phone_number = tables.Column(verbose_name=_("Teléfono"), accessor="phone_number")

    class Meta:
        model = Customer
        fields = ("full_name", "document_number", "email", "phone_number", "created_at", "actions")
