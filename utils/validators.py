from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def get_phone_valid_message():
    return str(_("Teléfono tiene que ser en el formato: '+999999999'. Se permiten hasta 15 dígitos."))


phone_expresion = r"\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$"
phone_regex_validator = RegexValidator(regex=phone_expresion, message=get_phone_valid_message())
color_regex_validator = RegexValidator(
    regex=r"^#(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})$", message=_("Hexadecimal Formato Incorrecto")
)

nie_expresion = r"[A-HJ-NP-SUVW][0-9]{7}[0-9A-J]|\d{8}[TRWAGMYFPDXBNJZSQVHLCKE]|[X]\d{7}[TRWAGMYFPDXBNJZSQVHLCKE]|[X]\d{8}[TRWAGMYFPDXBNJZSQVHLCKE]|[YZ]\d{0,7}[TRWAGMYFPDXBNJZSQVHLCKE]"
passport_expression = r"^(?!^0+$)[a-zA-Z0-9]{6,9}$"

