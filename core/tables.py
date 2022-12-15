import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from core.models import Author, Book, BookLoan


class AuthorTable(tables.Table):
    actions = tables.columns.TemplateColumn(
        verbose_name=_("Acciones"),
        template_name="core/author/actions.html",
        orderable=False,
    )
    full_name = tables.Column(verbose_name=_("Nombre"), accessor="full_name")

    class Meta:
        model = Author
        fields = ("full_name", "created_at", "actions")


class BookTable(tables.Table):
    actions = tables.columns.TemplateColumn(
        verbose_name=_("Acciones"),
        template_name="core/book/actions.html",
        orderable=False,
    )
    author = tables.columns.TemplateColumn(
        verbose_name=_("Autores"),
        template_name="core/book/authors.html",
        orderable=False,
    )
    title = tables.Column(verbose_name=_("Título"), accessor="title", orderable=True)
    quantity = tables.Column(verbose_name=_("Cantidad"), accessor="quantity", orderable=True)
    in_stock = tables.Column(verbose_name=_("En Stock"), accessor="in_stock", orderable=True)

    class Meta:
        model = Book
        fields = ("title", "author", "quantity", "in_stock", "actions")
        row_attrs = {
            'data-in_stock': lambda record: True if record.has_availability else False
        }


class BookLoanTable(tables.Table):
    actions = tables.columns.TemplateColumn(
        verbose_name=_("Acciones"),
        template_name="core/book_loan/actions.html",
        orderable=False,
    )
    books = tables.columns.TemplateColumn(
        verbose_name=_("Libros"),
        template_name="core/book_loan/books.html",
        orderable=False,
    )
    customer = tables.Column(verbose_name=_("Cliente"), accessor="customer", orderable=True)
    status = tables.Column(verbose_name=_("Estado"), accessor="status", orderable=True)
    end_date = tables.Column(verbose_name=_("Fecha de Entrega"), accessor="end_date", orderable=True)

    class Meta:
        model = BookLoan
        fields = ("customer", "books", "status", "end_date", "actions")
        row_attrs = {
            'data-status': lambda record: True if record.has_past else False
        }
