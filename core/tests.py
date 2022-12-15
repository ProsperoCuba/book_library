import datetime
from unittest import mock

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve

from core.filters import BookFilter, AuthorFilter, BookLoanFilter
from core.models import Book, Author, BookLoan
from customers.models import Customer

User = get_user_model()


class BookAccessTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)
        self.book = Book.objects.create(
            title="Libro Test", summary="test summary", quantity=5, in_stock=5
        )
        self.author = Author.objects.create(full_name="author1")
        self.book.author.add(self.author)

    def test_list_no_login(self):
        """Test access book what user anonymous"""
        url = reverse('core:books')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_list_admin(self):
        """Test access book what admin"""
        url = reverse('core:books')
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_create_no_login(self):
        """Test access book what user anonymous"""
        url = reverse('core:book_create')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_create_admin(self):
        """Test access book what admin"""
        url = reverse('core:book_create')
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_update_no_login(self):
        """Test access book what user anonymous"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_update_admin(self):
        """Test access book what admin"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 200)


class BookFilterTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)
        self.book = Book.objects.create(
            title="Libro Test", summary="test summary", quantity=5, in_stock=5
        )
        self.author = Author.objects.create(full_name="author1")
        self.book.author.add(self.author)

    def test_filter_search_title(self):
        """Test filters search by title"""
        GET = {'search': 'libro test'}
        f = BookFilter(GET, queryset=Book.objects.all())
        self.assertEqual(len(list(f.qs)), 1)

    def test_filter_search_summary(self):
        """Test filters search by summary"""
        GET = {'search': 'test summary'}
        f = BookFilter(GET, queryset=Book.objects.all())
        self.assertEqual(len(list(f.qs)), 1)


class BookTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)
        self.book = Book.objects.create(
            title="Libro Test", summary="test summary", quantity=5, in_stock=5
        )
        self.author = Author.objects.create(full_name="author1")
        self.book.author.add(self.author)

    def test_create_book_empty_field(self):
        """Test to create Book empty field"""
        url = reverse('core:book_create')
        data = {
            'title': '',
            'summary': '',
            'quantity': '',
            'in_stock': '',
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_title_field(self):
        """Test to create Book title field"""
        url = reverse('core:book_create')
        data = {
            'title': 'Libro winner',
            'summary': '',
            'quantity': '',
            'in_stock': '',
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_summary_field(self):
        """Test to create Book title field"""
        url = reverse('core:book_create')
        data = {
            'title': 'Libro winner',
            'summary': 'summary',
            'quantity': '',
            'in_stock': '',
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_quantity_field(self):
        """Test to create Book title, summary, quantity field"""
        url = reverse('core:book_create')
        data = {
            'title': 'Libro winner',
            'summary': 'summary',
            'quantity': 10,
            'in_stock': '',
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_in_stock_field(self):
        """Test to create Book title, summary, quantity, in_stock field"""
        url = reverse('core:book_create')
        data = {
            'title': 'Libro winner',
            'summary': 'summary',
            'quantity': 10,
            'in_stock': 10,
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)

    def test_create_book_author_field(self):
        """Test to create Book title, summary, quantity, in_stock, author field"""
        url = reverse('core:book_create')
        data = {
            'title': 'Libro winner',
            'summary': 'summary',
            'quantity': 10,
            'in_stock': 10,
            'author': [self.author.pk]
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_validate_in_stock_field(self):
        """Test to create Book validating that the in_stock is not greater than the quantity"""
        url = reverse('core:book_create')
        data = {
            'title': 'Libro winner',
            'summary': 'summary',
            'quantity': 10,
            'in_stock': 15,
            'author': [self.author.pk]
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)

    def test_update_book_empty_field(self):
        """Test to update Author empty field"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        data = {
            'title': '',
            'summary': '',
            'quantity': '',
            'in_stock': '',
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Libro Test')

    def test_update_book_title_field(self):
        """Test to update Author title field"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'updated',
            'summary': '',
            'quantity': '',
            'in_stock': '',
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Libro Test')

    def test_update_book_summary_field(self):
        """Test to update Author title, summary field"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'updated',
            'summary': 'update',
            'quantity': '',
            'in_stock': '',
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Libro Test')

    def test_update_book_quantity_field(self):
        """Test to update Author title, summary, quantity field"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'updated',
            'summary': 'update',
            'quantity': 10,
            'in_stock': '',
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Libro Test')

    def test_update_book_in_stock_field(self):
        """Test to update Author title, summary, quantity, in_stock field"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'updated',
            'summary': 'update',
            'quantity': 10,
            'in_stock': 10,
            'author': []
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Libro Test')

    def test_update_book_author_field(self):
        """Test to update Author title, summary, quantity, in_stock, author field"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'updated',
            'summary': 'updated',
            'quantity': 10,
            'in_stock': 10,
            'author': [self.author.pk]
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'updated')
        self.assertEqual(self.book.summary, 'updated')
        self.assertEqual(self.book.quantity, 10)
        self.assertEqual(self.book.in_stock, 10)

    def test_update_book_validate_in_stock_field(self):
        """Test to update Author validating that the in_stock is not greater than the quantity field"""
        url = reverse('core:book_update', kwargs={'pk': self.book.pk})
        data = {
            'title': 'updated',
            'summary': 'updated',
            'quantity': 10,
            'in_stock': 15,
            'author': [self.author.pk]
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book.pk)

        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Libro Test')


class AuthorAccessTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)

        self.author = Author.objects.create(full_name="author1")

    def test_list_no_login(self):
        """Test access author what user anonymous"""
        url = reverse('core:authors')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_list_admin(self):
        """Test access author what admin"""
        url = reverse('core:authors')
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_create_no_login(self):
        """Test access author what user anonymous"""
        url = reverse('core:author_create')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_create_admin(self):
        """Test access author what admin"""
        url = reverse('core:author_create')
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_update_no_login(self):
        """Test access author what user anonymous"""
        url = reverse('core:author_update', kwargs={'pk': self.author.pk})
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request, pk=self.author.pk)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_update_admin(self):
        """Test access author what admin"""
        url = reverse('core:author_update', kwargs={'pk': self.author.pk})
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.author.pk)

        self.assertEqual(response.status_code, 200)


class AuthorFilterTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)

        self.author = Author.objects.create(full_name="author1")

    def test_filter_search_full_name(self):
        """Test filters search by full_name"""
        GET = {'search': 'author1'}
        f = AuthorFilter(GET, queryset=Author.objects.all())
        self.assertEqual(len(list(f.qs)), 1)


class AuthorTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)

        self.author = Author.objects.create(full_name="author1")

    def test_create_author_empty_field(self):
        """Test to create Author empty field"""
        url = reverse('core:author_create')
        data = {
            'full_name': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Author.objects.count(), 1)

    def test_create_author_full_name_field(self):
        """Test to create Author full_name field"""
        url = reverse('core:author_create')
        data = {
            'full_name': 'Author Test'
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Author.objects.count(), 2)

    def test_update_author_empty_field(self):
        """Test to update Author empty field"""
        url = reverse('core:author_update', kwargs={'pk': self.author.pk})
        data = {
            'full_name': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.author.pk)

        self.assertEqual(response.status_code, 200)
        self.author.refresh_from_db()
        self.assertEqual(self.author.full_name, 'author1')

    def test_update_author_title_field(self):
        """Test to update Author title field"""
        url = reverse('core:author_update', kwargs={'pk': self.author.pk})
        data = {
            'full_name': 'updated'
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.author.pk)

        self.assertEqual(response.status_code, 302)
        self.author.refresh_from_db()
        self.assertEqual(self.author.full_name, 'updated')


class BookLoanAccessTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)
        self.customer = Customer.objects.create(document_number="654654", first_name="customer",
                                                last_name="last", email="customer@gmail.com")
        self.author = Author.objects.create(full_name="author1")
        self.book = Book.objects.create(title="book1", summary="summary1", quantity=5, in_stock=5)
        self.book.author.add(self.author)
        self.book_loan = BookLoan.objects.create(customer=self.customer, end_date="2022-10-10")
        self.book_loan.books.add(self.book)

    def test_list_no_login(self):
        """Test access book loan what user anonymous"""
        url = reverse('core:book_loans')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_list_admin(self):
        """Test access book loan what admin"""
        url = reverse('core:book_loans')
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_create_no_login(self):
        """Test access book loan what user anonymous"""
        url = reverse('core:book_loan_create')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_create_admin(self):
        """Test access book loan what admin"""
        url = reverse('core:book_loan_create')
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_update_no_login(self):
        """Test access book loan what user anonymous"""
        url = reverse('core:book_loan_update', kwargs={'pk': self.book_loan.pk})
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request, pk=self.book_loan.pk)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_update_admin(self):
        """Test access book loan what admin"""
        url = reverse('core:book_loan_update', kwargs={'pk': self.book_loan.pk})
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book_loan.pk)

        self.assertEqual(response.status_code, 200)


class BookLoanFilterTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)

        self.customer = Customer.objects.create(document_number="654654", first_name="customer",
                                                last_name="last", email="customer@gmail.com",
                                                phone_number="+59896101201")
        self.author = Author.objects.create(full_name="author1")
        self.book = Book.objects.create(title="book1", summary="summary1", quantity=5, in_stock=5)
        self.book.author.add(self.author)
        self.book_loan = BookLoan.objects.create(customer=self.customer, end_date="2022-10-10")
        self.book_loan.books.add(self.book)

    def test_filter_search_customer_first_name(self):
        """Test filters search by customer first_name"""
        GET = {'search': 'customer'}
        f = BookLoanFilter(GET, queryset=BookLoan.objects.all())
        self.assertEqual(len(list(f.qs)), 1)

    def test_filter_search_customer_last_name(self):
        """Test filters search by customer last_name"""
        GET = {'search': 'last'}
        f = BookLoanFilter(GET, queryset=BookLoan.objects.all())
        self.assertEqual(len(list(f.qs)), 1)

    def test_filter_search_customer_email(self):
        """Test filters search by customer email"""
        GET = {'search': 'customer@gmail.com'}
        f = BookLoanFilter(GET, queryset=BookLoan.objects.all())
        self.assertEqual(len(list(f.qs)), 1)

    def test_filter_search_customer_phone_number(self):
        """Test filters search by customer phone_number"""
        GET = {'search': '+59896101201'}
        f = BookLoanFilter(GET, queryset=BookLoan.objects.all())
        self.assertEqual(len(list(f.qs)), 1)

    def test_filter_search_status(self):
        """Test filters search by status"""
        GET = {'status': 'in_time'}
        f = BookLoanFilter(GET, queryset=BookLoan.objects.all())
        self.assertEqual(len(list(f.qs)), 1)


class BookLoanTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)

        self.customer = Customer.objects.create(document_number="654654", first_name="customer",
                                                last_name="last", email="customer@gmail.com",
                                                phone_number="+59896101201")
        self.customer1 = Customer.objects.create(document_number="654655", first_name="customer1",
                                                last_name="last1", email="customer1@gmail.com",
                                                phone_number="+59896101202")
        self.author = Author.objects.create(full_name="author1")
        self.book = Book.objects.create(title="book1", summary="summary1", quantity=5, in_stock=5)
        self.book.author.add(self.author)
        self.book_loan = BookLoan.objects.create(customer=self.customer, end_date="2022-10-10")
        self.book_loan.books.add(self.book)

    def test_create_book_loan_empty_field(self):
        """Test to create BookLoan empty field"""
        url = reverse('core:book_loan_create')
        data = {
            'customer': '',
            'books': '',
            'end_date': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookLoan.objects.count(), 1)

    def test_create_book_loan_customer_field(self):
        """Test to create BookLoan customer field"""
        url = reverse('core:book_loan_create')
        data = {
            'customer': self.customer.pk,
            'books': '',
            'end_date': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookLoan.objects.count(), 1)

    def test_create_book_loan_books_field(self):
        """Test to create BookLoan customer, books field"""
        url = reverse('core:book_loan_create')
        data = {
            'customer': self.customer.pk,
            'books': [self.book.pk],
            'end_date': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookLoan.objects.count(), 1)

    def test_create_book_loan_end_date_field(self):
        """Test to create BookLoan customer, books, end_date field"""
        url = reverse('core:book_loan_create')
        data = {
            'customer': self.customer.pk,
            'status': 'in_time',
            'books': [self.book.pk],
            'end_date': '2022-10-15'
        }
        request = self.factory.post(url, data)
        request.COOKIES = dict()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        request.user = self.superadmin
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookLoan.objects.count(), 2)

    def test_create_book_loan_check_in_stock(self):
        """Test to create BookLoan check in_stock"""
        url = reverse('core:book_loan_create')
        data = {
            'customer': self.customer.pk,
            'status': 'in_time',
            'books': [self.book.pk],
            'end_date': '2022-10-15'
        }
        request = self.factory.post(url, data)
        request.COOKIES = dict()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        request.user = self.superadmin
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookLoan.objects.count(), 2)
        self.book.refresh_from_db()
        self.assertEqual(self.book.in_stock, 4)

    def test_update_book_loan_empty_field(self):
        """Test to update BookLoan empty field"""
        url = reverse('core:book_loan_update', kwargs={'pk': self.book_loan.pk})
        data = {
            'status': '',
            'end_date': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book_loan.pk)

        self.assertEqual(response.status_code, 200)
        self.book_loan.refresh_from_db()
        self.assertEqual(self.book_loan.customer, self.customer)

    def test_update_book_loan_status_field(self):
        """Test to update BookLoan status field"""
        url = reverse('core:book_loan_update', kwargs={'pk': self.book_loan.pk})
        data = {
            'status': 'returned',
            'end_date': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.book_loan.pk)

        self.assertEqual(response.status_code, 200)
        self.book_loan.refresh_from_db()
        self.assertEqual(self.book_loan.status, "in_time")

    def test_update_book_loan_end_date_field(self):
        """Test to update BookLoan customer, end_date field"""
        url = reverse('core:book_loan_update', kwargs={'pk': self.book_loan.pk})
        data = {
            'status': 'returned',
            'end_date': '2022-10-15'
        }
        request = self.factory.post(url, data)
        request.COOKIES = dict()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        request.user = self.superadmin
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        view = resolve(url).func
        response = view(request, pk=self.book_loan.pk)

        self.assertEqual(response.status_code, 302)
        self.book_loan.refresh_from_db()
        self.assertEqual(self.book_loan.status, 'returned')

    def test_update_book_loan_approved_delivery_field(self):
        """Test to update BookLoan approved_delivery"""
        url = reverse('core:approved_delivery', kwargs={'book_loan_id': self.book_loan.pk})
        request = self.factory.post(url)
        request.COOKIES = dict()
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        request.user = self.superadmin
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        view = resolve(url).func
        response = view(request, book_loan_id=self.book_loan.pk)

        self.assertEqual(response.status_code, 302)
        self.book_loan.refresh_from_db()
        self.book.refresh_from_db()
        self.assertEqual(self.book_loan.status, 'returned')
        self.assertEqual(self.book.in_stock, 6)
