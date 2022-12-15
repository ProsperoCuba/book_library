from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from utils.mixins import LowercaseEmailField
from utils.models import AbstractDates
from utils.validators import get_phone_valid_message, phone_regex_validator

User = get_user_model()


class Customer(AbstractDates):
    """Model where clients are managed"""
    document_number = models.CharField(verbose_name=_("DNI/NIE/Pasaporte"), max_length=15, unique=True)
    first_name = models.CharField(verbose_name=_("Nombre"), max_length=150)
    last_name = models.CharField(verbose_name=_("Apellidos"), max_length=250)
    email = LowercaseEmailField(verbose_name=_("Correo"), max_length=128, blank=True, null=True)
    phone_number = models.CharField(
        verbose_name=_("Teléfono"),
        max_length=16,
        blank=True,
        null=True,
        validators=[phone_regex_validator],
        help_text=get_phone_valid_message(),
    )

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")
        ordering = ["-created_at"]
        permissions = (("manage_customer", _("Puede Administrar Cliente")),)

    def get_edit_url(self):
        """Return customer edit url."""
        return reverse_lazy("customers:customers_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        """Return customer delete url."""
        return reverse_lazy("customers:customers_delete", kwargs={"pk": self.pk})

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def has_book_loan(self, cant=None):
        """
        Method to know if you can lend more books to the client.
        :param cant: <boolean> if you want to return the amount
        """
        aux = 0
        for book_loan in self.book_loan.filter(status__in=['in_time', 'past']):
            aux += book_loan.books.count()

        if cant:
            return aux

        return aux < 3
