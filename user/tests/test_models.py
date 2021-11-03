from django.test import TestCase, Client
from user.serializers import CreateUserSerializer
from user.models import VirtualWalletUser


class ModelsTest(TestCase):
    def setUp(self):
        self.user = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='test_create@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )
        self.client = Client()

    def test_User_model_regular_user(self):
        self.user = VirtualWalletUser.objects.create(
            email='myemail@test.com',
            password='aA987654321',
            first_name='User',
            last_name='Test',
            birth_date='2000-01-01'
        )

    def test_User_model_superuser(self):
        self.user = VirtualWalletUser.objects.create(
            email='myemail@test.com',
            password='aA987654321',
            first_name='User',
            last_name='Test',
            birth_date='2000-01-01',
            is_superuser=True
        )

    def tearDown(self):
        self.user = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='test_delete@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )
        self.user.delete()
