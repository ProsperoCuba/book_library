from django import forms
from django.utils.translation import gettext_lazy as _
from customers.models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ["document_number", "first_name", "last_name", "email", "phone_number"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"placeholder": _("example@gmail.com"), "autocomplete": "off"}
            ),
            "document_number": forms.TextInput(
                attrs={
                    "placeholder": _(
                        "Entre el número de identidad"
                    ),
                    "autocomplete": "off",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "+999999999", "autocomplete": "off", "type": "tel"},
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": _("Entre su Nombre"), "autocomplete": "off"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": _("Entre sus Apellidos"), "autocomplete": "off"}
            ),

        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number:
            return phone_number.replace(" ", "")

    def clean_document_number(self):
        document_number = self.cleaned_data.get("document_number")
        return document_number.replace(" ", "")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            return email.lower().strip()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")
        document_number = cleaned_data.get("document_number")

        qs_base = Customer.objects.all()

        if self.instance and self.instance.pk:
            qs_base = qs_base.exclude(pk=self.instance.pk)

        email_valid = not qs_base.filter(email=email).exists()
        phone_valid = not qs_base.filter(phone_number=phone_number).exists()
        dni_valid = not qs_base.filter(document_number=document_number).exists()

        if not email and not phone_number:
            self.add_error("email", _("Debe proporcionarse un teléfono o un correo como medio de contacto."))
            self.add_error("phone_number", _("Debe proporcionarse un teléfono o un correo como medio de contacto."))

        if email and not email_valid:
            self.add_error("email", _("Este correo ya está en uso."))

        if phone_number and not phone_valid:
            self.add_error("phone_number", _("Este teléfono ya está en uso."))

        if not dni_valid:
            self.add_error(
                "document_number", _("Este número de documento ya está en uso.")
            )

        if self.errors:
            self.add_error(
                None,
                _(
                    "Usted tiene algunos errores en su información, por favor, corríjalos."
                ),
            )



        return cleaned_data