from django.urls import path

from customers.views import CustomerListView, CustomerCreateView, CustomerDeleteView, CustomerUpdateView

app_name = "customers"

urlpatterns = [
    path("customers", CustomerListView.as_view(), name="customers"),
    path("customer/create", CustomerCreateView.as_view(), name="customers_create"),
    path("customers/<int:pk>/update", CustomerUpdateView.as_view(), name="customers_update"),
    path("customers/<int:pk>/delete", CustomerDeleteView.as_view(), name="customers_delete"),
]
