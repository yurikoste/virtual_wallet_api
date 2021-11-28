from django.test import TestCase, Client
from transactions.serializers import FillSerializer
from user.models import VirtualWalletUser
from transactions.models import Wallet, Transaction


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

    def test_Wallet_model(self):
        self.wallet = Wallet.objects.create(
            owner=self.user,
            balance='111',
            last_used_currency='UAH'
        )

    def test_Transaction_model(self):
        self.wallet = Wallet.objects.create(
            owner=self.user,
            balance='111',
            last_used_currency='UAH'
        )
        transaction = Transaction.objects.create(
            wallet=self.wallet,
            email='test_create@example.com',
            type='payment_received',
            value=100
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
