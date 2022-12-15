from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from customers.filters import CustomerFilter
from customers.forms import CustomerForm
from customers.models import Customer
from customers.tables import CustomerTable


class CustomerListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """
    ListView for the model Customer.
    """
    model = Customer
    template_name = "customers/customer_list.html"
    table_class = CustomerTable
    filterset_class = CustomerFilter
    paginate_by = 25


class CustomerCreateView(LoginRequiredMixin, CreateView):
    """
    CreateView for the model Customer.
    """
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_create.html"
    success_url = reverse_lazy('customers:customers')


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """
    UpdateView for the model Customer.
    """
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_edit.html"
    success_url = reverse_lazy("customers:customers")


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    """
    DeleteView for the model Customer.
    """
    model = Customer
    template_name = "common/delete_object.html"
    success_url = reverse_lazy("customers:customers")
