from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order

class DashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.normal_user = User.objects.create_user('user', 'user@test.com', 'password')
        Order.objects.create(full_name='Order 1', tracking_id='11111111-1111-1111-1111-111111111111')
        Order.objects.create(full_name='Order 2', tracking_id='22222222-2222-2222-2222-222222222222')

    def test_dashboard_access_superuser(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total Orders')
        self.assertContains(response, '2') # Total orders count

    def test_dashboard_access_denied_normal_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('admin_dashboard'))
        # Should redirect to login (default behavior of user_passes_test if not logged in or fails test typically redirects to login url)
        # Note: if login_url is not set, defaults to /accounts/login/
        self.assertEqual(response.status_code, 302) 

    def test_dashboard_access_denied_anonymous(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)
