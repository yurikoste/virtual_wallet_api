from django.test import TestCase, Client
from rest_framework.test import force_authenticate, APIRequestFactory
from user.models import VirtualWalletUser


class ViewsTesting(TestCase):
    def setUp(self):
        self.user = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='test_create@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )
        self.client = Client()

    def test_signup(self):
        data = {
            'password': 'aA987654321',
            'email': 'test_create1@example.com',
            'first_name': 'User',
            'last_name': 'Test',
            'birth_date': '1987-08-30'
        }
        response = self.client.post('/api/v1/user/signup/', data)
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        self.user = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='test_delete@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )
        self.user.delete()
