from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve

from customers.filters import CustomerFilter
from customers.models import Customer

User = get_user_model()


class CustomerAccessTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)
        self.customer = Customer.objects.create(
            document_number="456465", first_name="customer test", last_name="last", email="customer@gmail.com"
        )

    def test_list_no_login(self):
        """Test access customer what user anonymous"""
        url = reverse('customers:customers')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_list_admin(self):
        """Test access customer what admin"""
        url = reverse('customers:customers')
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_create_no_login(self):
        """Test access customer what user anonymous"""
        url = reverse('customers:customers_create')
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_create_admin(self):
        """Test access customer what admin"""
        url = reverse('customers:customers_create')
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_update_no_login(self):
        """Test access customer what user anonymous"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        request = self.factory.get(url)
        request.user = AnonymousUser()
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        # redirect to login
        self.assertEqual(response.status_code, 302)

    def test_update_admin(self):
        """Test access customer what admin"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        request = self.factory.get(url)
        request.COOKIES = dict()
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        self.assertEqual(response.status_code, 200)


class CustomerFilterTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)
        self.customer = Customer.objects.create(
            document_number="456465", first_name="customer test", last_name="last", email="customer@gmail.com"
        )

    def test_filter_search_first_name(self):
        """Test filters search by first_name"""
        GET = {'search': 'customer test'}
        f = CustomerFilter(GET, queryset=Customer.objects.all())
        self.assertEqual(len(list(f.qs)), 1)

    def test_filter_search_last_name(self):
        """Test filters search by last_name"""
        GET = {'search': 'last'}
        f = CustomerFilter(GET, queryset=Customer.objects.all())
        self.assertEqual(len(list(f.qs)), 1)

    def test_filter_search_email(self):
        """Test filters search by email"""
        GET = {'search': 'customer@gmail.com'}
        f = CustomerFilter(GET, queryset=Customer.objects.all())
        self.assertEqual(len(list(f.qs)), 1)

    def test_filter_search_document_number(self):
        """Test filters search by document_number"""
        GET = {'search': '456465'}
        f = CustomerFilter(GET, queryset=Customer.objects.all())
        self.assertEqual(len(list(f.qs)), 1)


class CustomerTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superadmin = User.objects.create(email='superadmin@gmail.com', first_name='superadmin',
                                              last_name='superadmin', is_active=True, is_superuser=True)
        self.customer = Customer.objects.create(
            document_number="456465", first_name="customer test", last_name="last", email="customer@gmail.com"
        )

    def test_create_customer_empty_field(self):
        """Test to create Customer empty field"""
        url = reverse('customers:customers_create')
        data = {
            'document_number': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)

    def test_create_customer_document_number_field(self):
        """Test to create Customer with document_number"""
        url = reverse('customers:customers_create')
        data = {
            'document_number': '546546545',
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)

    def test_create_customer_first_name_field(self):
        """Test to create Customer with document_number, first_name"""
        url = reverse('customers:customers_create')
        data = {
            'document_number': '546546545',
            'first_name': 'test',
            'last_name': '',
            'email': '',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)

    def test_create_customer_last_name_field(self):
        """Test to create Customer with document_number, first_name, last_name"""
        url = reverse('customers:customers_create')
        data = {
            'document_number': '546546545',
            'first_name': 'test',
            'last_name': 'test',
            'email': '',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)

    def test_create_customer_email_field(self):
        """Test to create Customer with document_number, first_name, last_name, email"""
        url = reverse('customers:customers_create')
        data = {
            'document_number': '546546545',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@gmail.com',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 2)

    def test_create_customer_phone_number_field(self):
        """Test to create Customer with document_number, first_name, last_name, phone_numer"""
        url = reverse('customers:customers_create')
        data = {
            'document_number': '546546545',
            'first_name': 'test',
            'last_name': 'test',
            'email': '',
            'phone_number': '+59896101501'
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 2)

    def test_create_customer_phone_number_email_field(self):
        """Test to create Customer with document_number, first_name, last_name, email, phone_numer"""
        url = reverse('customers:customers_create')
        data = {
            'document_number': '546546545',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@gmail.com',
            'phone_number': '+59896101501'
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 2)

    def test_update_customer_empty_field(self):
        """Test to update Customer empty field"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        data = {
            'document_number': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'customer test')

    def test_update_customer_document_number_field(self):
        """Test to update Customer document_number field"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        data = {
            'document_number': '546654',
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'customer test')
        self.assertEqual(self.customer.document_number, '456465')

    def test_update_customer_first_name_field(self):
        """Test to update Customer document_number, first_name field"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        data = {
            'document_number': '546654',
            'first_name': 'test',
            'last_name': '',
            'email': '',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'customer test')
        self.assertEqual(self.customer.document_number, '456465')

    def test_update_customer_last_name_field(self):
        """Test to update Customer document_number, first_name, last_name field"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        data = {
            'document_number': '546654',
            'first_name': 'test',
            'last_name': 'test',
            'email': '',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'customer test')
        self.assertEqual(self.customer.document_number, '456465')

    def test_update_customer_email_field(self):
        """Test to update Customer document_number, first_name, last_name, email field"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        data = {
            'document_number': '546654',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@gmail.com',
            'phone_number': ''
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        self.assertEqual(response.status_code, 302)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'test')
        self.assertEqual(self.customer.document_number, '546654')
        self.assertEqual(self.customer.email, 'test@gmail.com')

    def test_update_customer_phone_number_field(self):
        """Test to update Customer document_number, first_name, last_name, phone_number field"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        data = {
            'document_number': '546654',
            'first_name': 'test',
            'last_name': 'test',
            'email': '',
            'phone_number': '+59896101701'
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        self.assertEqual(response.status_code, 302)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'test')
        self.assertEqual(self.customer.document_number, '546654')
        self.assertEqual(self.customer.phone_number, '+59896101701')

    def test_update_customer_phone_number_email_field(self):
        """Test to update Customer document_number, first_name, last_name, email, phone_number field"""
        url = reverse('customers:customers_update', kwargs={'pk': self.customer.pk})
        data = {
            'document_number': '546654',
            'first_name': 'test',
            'last_name': 'test',
            'email': '',
            'phone_number': '+59896101701'
        }
        request = self.factory.post(url, data)
        request.user = self.superadmin
        view = resolve(url).func
        response = view(request, pk=self.customer.pk)

        self.assertEqual(response.status_code, 302)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'test')
        self.assertEqual(self.customer.document_number, '546654')
        self.assertEqual(self.customer.phone_number, '+59896101701')


