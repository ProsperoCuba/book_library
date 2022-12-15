import django_tables2 as tables
from django.contrib.auth.forms import AdminPasswordChangeForm, UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, UpdateView
from django_filters.views import FilterView

from .forms import UserForm
from .models import User
from .tables import UserTable
from .filters import UserFilter


class IsSuperUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class UserListView(IsSuperUserMixin, tables.SingleTableMixin, FilterView):
    table_class = UserTable
    queryset = User.objects.filter(is_removed=False)
    filterset_class = UserFilter
    template_name = "users/user_list.html"


class UserEditView(IsSuperUserMixin, UpdateView):
    model = User
    queryset = User.objects.filter(is_removed=False)
    fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_superuser",
        "is_active",
    )
    template_name = "users/user_edit.html"
    success_url = reverse_lazy("users:users")


class UserPasswordView(IsSuperUserMixin, FormView):
    form_class = AdminPasswordChangeForm
    template_name = "users/user_password.html"
    success_url = reverse_lazy("users:users")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, pk=self.kwargs["pk"])
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        if self.request.method == "GET":
            form = form_class(get_object_or_404(User, pk=self.kwargs["pk"]))
        else:
            form = form_class(get_object_or_404(User, pk=self.kwargs["pk"]), self.request.POST)
        return form

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserDeleteView(IsSuperUserMixin, DeleteView):
    model = User
    template_name = "common/delete_object.html"
    success_url = reverse_lazy("users:users")

    def form_valid(self, form):
        user = self.get_object()
        user.is_active = False
        user.save()
        return super().form_valid(form)


class UserCreationView(IsSuperUserMixin, CreateView):
    form_class = UserForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("users:users")
