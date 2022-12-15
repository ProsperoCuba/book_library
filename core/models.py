from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from core.enums import StatusBookLoanOptions
from customers.models import Customer
from utils.models import AbstractDates

User = get_user_model()


class Author(AbstractDates):
    """Model where authors are managed"""
    full_name = models.CharField(verbose_name=_("Nombre y Apellidos"), max_length=250)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("Autor")
        verbose_name_plural = _("Autores")
        ordering = ["-created_at"]
        permissions = (("manage_author", _("Puede Administrar Autores")),)

    def get_edit_url(self):
        """Return author edit url."""
        return reverse_lazy("core:author_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        """Return author delete url."""
        return reverse_lazy("core:author_delete", kwargs={"pk": self.pk})


class Book(AbstractDates):
    """Model where books are managed"""
    title = models.CharField(verbose_name=_("Título"), max_length=150)
    summary = models.CharField(verbose_name=_("Resumen"), max_length=500, blank=True, null=True)
    author = models.ManyToManyField(Author, verbose_name=_('Autor'), related_name="books")
    quantity = models.PositiveIntegerField(verbose_name=_('Cantidad de Ejemplares'), default=1)
    in_stock = models.PositiveIntegerField(verbose_name=_('Cantidad Disponible'), default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Libro")
        verbose_name_plural = _("Libros")
        ordering = ["-created_at"]
        permissions = (("manage_book", _("Puede Administrar Libros")),)

    def clean(self):
        """Validating that there are no more books in stock than the number of copies"""
        if self.quantity < self.in_stock:
            raise ValidationError({'in_stock': _('La cantidad de libros en stock no pueden ser mayor a la cantidad de ejemplares.')})

    def get_edit_url(self):
        """Return book edit url."""
        return reverse_lazy("core:book_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        """Return book delete url."""
        return reverse_lazy("core:book_delete", kwargs={"pk": self.pk})

    @property
    def get_authors(self):
        """Returns the list of authors."""
        return [item.full_name for item in self.author.all()]

    @property
    def has_availability(self):
        """Method to know if the book is available."""
        return self.in_stock > 0


class BookLoan(AbstractDates):
    """Model where loans are managed"""
    customer = models.ForeignKey(Customer, verbose_name=_('Cliente'), on_delete=models.CASCADE,
                                 related_name="book_loan")
    books = models.ManyToManyField(Book, verbose_name=_('Libros'), related_name="book_loan")
    status = models.CharField(verbose_name=_('Estado'), choices=StatusBookLoanOptions.choices,
                              default=StatusBookLoanOptions.in_time, max_length=8)
    end_date = models.DateField(verbose_name=_("Fecha de Entrega"))

    def __str__(self):
        return "{} - {} - {}".format(self.customer.__str__(), self.status, self.end_date)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_status = self.status

    class Meta:
        verbose_name = _("Préstamo")
        verbose_name_plural = _("Préstamos")
        ordering = ["-created_at"]
        permissions = (("manage_book_loan", _("Puede Administrar Préstamos")),)

    @property
    def status_has_changed(self):
        return self._initial_status != self.status

    def get_edit_url(self):
        """Return book_loan edit url."""
        return reverse_lazy("core:book_loan_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        """Return book_loan delete url."""
        return reverse_lazy("core:book_loan_delete", kwargs={"pk": self.pk})

    @property
    def get_books(self):
        """Returns the list of books."""
        return [book.title for book in self.books.all()]

    def approved_delivery(self):
        return reverse_lazy("core:approved_delivery", kwargs={"book_loan_id": self.pk})

    @property
    def has_past(self):
        """Find out if there are any loans in arrears."""
        return self.status == 'past'

