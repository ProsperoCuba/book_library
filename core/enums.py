from django.utils.translation import gettext_lazy as _

from utils.enums import Enum


CHOICES_BOOLEAN_FILTER = (
    (0, _("No")),
    (1, _("Sí")),
)


class StatusBookLoanOptions(Enum):
    in_time = _("En Tiempo")
    returned = _("Entregado")
    past = _("Fuera de Tiempo")

