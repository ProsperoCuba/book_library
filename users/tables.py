import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from .models import User


class UserTable(tables.Table):
    actions = tables.columns.TemplateColumn(
        verbose_name=_("Acciones"),
        template_name="users/actions.html",
        orderable=False,
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "is_superuser", "is_active", "date_joined")
