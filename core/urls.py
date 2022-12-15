from django.urls import path

from core.views import AuthorListView, AuthorCreateView, AuthorUpdateView, AuthorDeleteView, BookListView, \
    BookCreateView, BookUpdateView, BookDeleteView, BookLoanListView, BookLoanCreateView, BookLoanUpdateView, \
    BookLoanDeleteView, approve_delivery

app_name = "core"

urlpatterns = [
    # Urls for the model Author (Class Based Views)
    path("authors", AuthorListView.as_view(), name="authors"),
    path("authors/create", AuthorCreateView.as_view(), name="author_create"),
    path("authors/<int:pk>/update", AuthorUpdateView.as_view(), name="author_update"),
    path("authors/<int:pk>/delete", AuthorDeleteView.as_view(), name="author_delete"),

    # Urls for the model Book (Class Based Views)
    path("books", BookListView.as_view(), name="books"),
    path("books/create", BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/update", BookUpdateView.as_view(), name="book_update"),
    path("books/<int:pk>/delete", BookDeleteView.as_view(), name="book_delete"),

    # Urls for the model BookLoan (Class Based Views)
    path("", BookLoanListView.as_view(), name="book_loans"),
    path("book_loans/create", BookLoanCreateView.as_view(), name="book_loan_create"),
    path("book_loans/<int:pk>/update", BookLoanUpdateView.as_view(), name="book_loan_update"),
    path("book_loans/<int:pk>/delete", BookLoanDeleteView.as_view(), name="book_loan_delete"),
    path("book_loans/<int:book_loan_id>/approved", approve_delivery, name="approved_delivery")
]
