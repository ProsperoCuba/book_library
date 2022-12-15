from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractDates(models.Model):
    """
    Abstract model for add creation and update times for records
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Creación"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Fecha de Actualización"))

    class Meta:
        abstract = True
