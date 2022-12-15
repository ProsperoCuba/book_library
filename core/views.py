from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django.utils.translation import gettext_lazy as _

from core.enums import StatusBookLoanOptions
from core.filters import AuthorFilter, BookFilter, BookLoanFilter
from core.forms import AuthorForm, BookForm, BookLoanForm, BookLoanUpdateForm
from core.models import Author, Book, BookLoan
from core.tables import AuthorTable, BookTable, BookLoanTable
from core.utils import update_stock, update_status


class AuthorListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """
    ListView for the model Author.
    """
    model = Author
    template_name = "core/author/author_list.html"
    table_class = AuthorTable
    filterset_class = AuthorFilter
    paginate_by = 25


class AuthorCreateView(LoginRequiredMixin, CreateView):
    """
    CreateView for the model Author.
    """
    model = Author
    form_class = AuthorForm
    template_name = "core/author/author_create.html"
    success_url = reverse_lazy('core:authors')


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    """
    UpdateView for the model Author.
    """
    model = Author
    form_class = AuthorForm
    template_name = "core/author/author_edit.html"
    success_url = reverse_lazy("core:authors")


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    """
    DeleteView for the model Author.
    """
    model = Author
    template_name = "common/delete_object.html"
    success_url = reverse_lazy("core:authors")


class BookListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """
    ListView for the model Book.
    """
    model = Book
    template_name = "core/book/book_list.html"
    table_class = BookTable
    filterset_class = BookFilter
    paginate_by = 10


class BookCreateView(LoginRequiredMixin, CreateView):
    """
    CreateView for the model Book.
    """
    model = Book
    form_class = BookForm
    template_name = "core/book/book_create.html"
    success_url = reverse_lazy('core:books')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    """
    UpdateView for the model Book.
    """
    model = Book
    form_class = BookForm
    template_name = "core/book/book_edit.html"
    success_url = reverse_lazy("core:books")


class BookDeleteView(LoginRequiredMixin, DeleteView):
    """
    DeleteView for the model Book.
    """
    model = Book
    template_name = "common/delete_object.html"
    success_url = reverse_lazy("core:books")


class BookLoanListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """
    ListView for the model BookLoan.
    """
    model = BookLoan
    template_name = "core/book_loan/book_loan_list.html"
    table_class = BookLoanTable
    filterset_class = BookLoanFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_status()

        return context


class BookLoanCreateView(LoginRequiredMixin, CreateView):
    """
    CreateView for the model BookLoan.
    """
    model = BookLoan
    form_class = BookLoanForm
    template_name = "core/book_loan/book_loan_create.html"
    success_url = reverse_lazy('core:book_loans')

    def form_valid(self, form):
        self.object = form.save()
        update_stock(self.object.books, less=True)
        messages.success(self.request, _("Se ha creado el préstamo correctamente!"))
        return redirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(BookLoanCreateView, self).get_form_kwargs()
        kwargs['books_qs'] = Book.objects.filter(in_stock__gt=0)
        return kwargs


class BookLoanUpdateView(LoginRequiredMixin, UpdateView):
    """
    UpdateView for the model Book.
    """
    model = BookLoan
    form_class = BookLoanUpdateForm
    template_name = "core/book_loan/book_loan_edit.html"
    success_url = reverse_lazy("core:book_loans")

    def form_valid(self, form):
        self.object = form.save()
        if self.object.status_has_changed:
            if self.object._initial_status == "returned":
                update_stock(self.object.books, less=True)
            elif self.object._initial_status in ['in_time', 'past'] and self.object.status == 'returned':
                update_stock(self.object.books)
        messages.success(self.request, _('Se ha actualizado correctamente el préstamo.'))
        return redirect(self.success_url)


class BookLoanDeleteView(LoginRequiredMixin, DeleteView):
    """
    DeleteView for the model BookLoan.
    """
    model = BookLoan
    template_name = "common/delete_object.html"
    success_url = reverse_lazy("core:book_loans")

    def form_valid(self, form):
        success_url = self.get_success_url()
        object = self.object
        if object.status != 'returned':
            messages.warning(self.request, _("No se puede eliminar el préstamo si no se ha devuelto los libros."))
        else:
            self.object.delete()
            messages.success(self.request, _("Se ha eliminado el préstamo correctamente!"))
        return HttpResponseRedirect(success_url)


@login_required()
def approve_delivery(request, book_loan_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["post"])
    book_loan = get_object_or_404(BookLoan, pk=book_loan_id)
    book_loan.status = StatusBookLoanOptions.returned
    book_loan.save()
    update_stock(book_loan.books)
    messages.success(request, _("Se aprobó la entrega del préstamo correctamente!"))
    return redirect(reverse_lazy('core:book_loans'))
