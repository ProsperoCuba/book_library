from django.db import models


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def get_prep_value(self, value):
        value = super(LowercaseEmailField, self).get_prep_value(value)
        if isinstance(value, str):
            return value.lower()
        return value


class CustomizableCharField(models.CharField):
    """Customizable Char field for allow configure (lower | upper) and (strip | replace) settings"""

    def __init__(self, *args, **kwargs):
        self.is_uppercase = kwargs.pop("uppercase", False)
        self.is_lowercase = kwargs.pop("lowercase", False)
        self.is_strip = kwargs.pop("strip", False)
        self.is_remove_blanks = kwargs.pop("remove_blanks", False)
        self.is_replace_blanks = kwargs.pop("replace_blanks", False)
        self.replace_blanks_value = kwargs.pop("replace_blanks_value", "_")
        super(CustomizableCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super(CustomizableCharField, self).get_prep_value(value)

        if isinstance(value, str):
            if self.is_remove_blanks:
                value = value.replace(" ", "")
            elif self.is_replace_blanks:
                rep = self.replace_blanks_value or "_"
                value = value.replace(" ", rep)
            elif self.is_strip:
                value = value.strip()

            if self.is_uppercase:
                value = value.upper()
            elif self.is_lowercase:
                value = value.lower()

        return value
