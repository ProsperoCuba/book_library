from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel

from utils.mixins import LowercaseEmailField
from utils.validators import get_phone_valid_message, phone_regex_validator


class User(AbstractUser, SoftDeletableModel):

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("Usuario"),
        max_length=150,
        help_text=_("Sólo 150 caracteres o menos, Letras, dígitos y @/./+/-/_"),
        null=True,
        unique=True,
        validators=[username_validator],
    )
    email = LowercaseEmailField(verbose_name=_("Correo"), unique=True)
    phone_number = models.CharField(
        verbose_name=_("Teléfono"),
        unique=True,
        max_length=16,
        blank=True,
        null=True,
        validators=[phone_regex_validator],
        help_text=get_phone_valid_message(),
    )

    def __str__(self):
        return self.get_full_name() or self.email or "{} #{}".format(str(_("Usuario")), self.pk)

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ("-date_joined", "email")

    @property
    def formatted_name(self):
        full_name = self.__str__()
        if full_name:
            pieces = full_name.split()
            name = pieces.pop(0)
            if pieces:
                abb = " ".join(["{}.".format(i[0].upper()) for i in pieces])
                name = f"{name} {abb}"
            return name
        return self.email if self.email else self.username
