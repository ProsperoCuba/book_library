from django.urls import path

from .views import UserCreationView, UserDeleteView, UserEditView, UserListView, UserPasswordView

app_name = "users"

urlpatterns = [
    path("edit/<int:pk>", UserEditView.as_view(), name="edit"),
    path("password/<int:pk>", UserPasswordView.as_view(), name="password"),
    path("delete/<int:pk>", UserDeleteView.as_view(), name="delete"),
    path("create/", UserCreationView.as_view(), name="create"),
    path("", UserListView.as_view(), name="users"),
]
