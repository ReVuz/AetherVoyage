from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from .forms import CustomUserCreationForm
from .decorators import role_required, admin_required, staff_required, customer_required

# Stub view to test decorators
def dummy_view(request):
    return HttpResponse("Success")

class CustomUserModelTest(TestCase):
    def test_user_creation_with_roles(self):
        # Create Customer
        customer = CustomUser.objects.create_user(username='cust', email='cust@test.com', password='pass123', role='customer')
        self.assertTrue(customer.is_customer)
        self.assertFalse(customer.is_staff_member)
        self.assertFalse(customer.is_admin)

        # Create Staff
        staff = CustomUser.objects.create_user(username='stf', email='stf@test.com', password='pass123', role='staff')
        self.assertFalse(staff.is_customer)
        self.assertTrue(staff.is_staff_member)
        self.assertFalse(staff.is_admin)

        # Create Admin
        admin = CustomUser.objects.create_user(username='adm', email='adm@test.com', password='pass123', role='admin')
        self.assertFalse(admin.is_customer)
        self.assertTrue(admin.is_staff_member)
        self.assertTrue(admin.is_admin)

class CustomUserCreationFormTest(TestCase):
    def test_form_saves_roles_correctly(self):
        # Customer Role signup
        data_customer = {
            'username': 'customer1',
            'email': 'customer1@test.com',
            'role': 'customer',
            'password1': 'AetherVoyage2026!',
            'password2': 'AetherVoyage2026!',
        }
        form = CustomUserCreationForm(data=data_customer)
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save(commit=False)
        self.assertEqual(user.role, 'customer')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Staff Role signup
        data_staff = {
            'username': 'staff1',
            'email': 'staff1@test.com',
            'role': 'staff',
            'password1': 'AetherVoyage2026!',
            'password2': 'AetherVoyage2026!',
        }
        form_staff = CustomUserCreationForm(data=data_staff)
        self.assertTrue(form_staff.is_valid(), form_staff.errors)
        user_staff = form_staff.save(commit=False)
        self.assertEqual(user_staff.role, 'staff')
        self.assertTrue(user_staff.is_staff)
        self.assertFalse(user_staff.is_superuser)

class MockMessages:
    def __init__(self):
        self.messages = []
    def add(self, level, message, extra_tags=''):
        self.messages.append(message)

class DecoratorsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.customer = CustomUser.objects.create_user(username='cust', email='cust@test.com', password='pass123', role='customer')
        self.staff = CustomUser.objects.create_user(username='stf', email='stf@test.com', password='pass123', role='staff')
        self.admin = CustomUser.objects.create_user(username='adm', email='adm@test.com', password='pass123', role='admin')
        
    def test_customer_only_access(self):
        protected_view = customer_required(dummy_view)
        
        # Test Customer access
        request = self.factory.get('/dummy/')
        request.user = self.customer
        response = protected_view(request)
        self.assertEqual(response.status_code, 200)
        
        # Test Staff block (redirects)
        request.user = self.staff
        request._messages = MockMessages()
        response = protected_view(request)
        self.assertEqual(response.status_code, 302)

    def test_staff_access(self):
        protected_view = staff_required(dummy_view)
        
        # Test Staff access
        request = self.factory.get('/dummy/')
        request.user = self.staff
        response = protected_view(request)
        self.assertEqual(response.status_code, 200)
        
        # Test Admin access (allowed)
        request.user = self.admin
        response = protected_view(request)
        self.assertEqual(response.status_code, 200)

        # Test Customer block (redirects)
        request.user = self.customer
        request._messages = MockMessages()
        response = protected_view(request)
        self.assertEqual(response.status_code, 302)
