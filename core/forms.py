from django import forms
from django.utils.translation import gettext_lazy as _

from core.models import Author, Book, BookLoan
from core.utils import get_min_date


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ["full_name"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"placeholder": _("Entre su Nombre Completo"), "autocomplete": "off"}
            )
        }


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ["title", "summary", "author", "quantity", "in_stock"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": _("Entre un título"), "autocomplete": "off"}
            ),
            "summary": forms.Textarea(
                attrs={"placeholder": _("Entre un resumen"), "autocomplete": "off", "cols": 1, "rows": 5}
            ),
            "quantity": forms.TextInput(
                attrs={"placeholder": _("Entre cantidad de ejemplares"), "autocomplete": "off"}
            ),
            "in_stock": forms.TextInput(
                attrs={"placeholder": _("Entre cantidad en stock"), "autocomplete": "off"}
            )
        }


class BookLoanForm(forms.ModelForm):

    class Meta:
        model = BookLoan
        fields = ["customer", "books", "status", "end_date"]

        widgets = {
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": get_min_date(),
                    "autocomplete": "off"
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get("customer")
        books = cleaned_data.get("books")

        if customer and not customer.has_book_loan():
            self.add_error("customer", _("Este cliente supera el limite de libros prestados."))
        elif books:
            if books.count() + customer.has_book_loan(cant=True) > 3:
                self.add_error("books", _("Solo es permitido prestar 3 libros."))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        books_qs = kwargs.pop('books_qs', None)
        super(BookLoanForm, self).__init__(*args, **kwargs)
        if books_qs is not None:
            self.fields['books'].queryset = books_qs


class BookLoanUpdateForm(forms.ModelForm):

    class Meta:
        model = BookLoan
        fields = ["status", "end_date"]

        widgets = {
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": get_min_date(),
                    "autocomplete": "off"
                }
            )
        }
