from django.test import TestCase

from user.models import VirtualWalletUser
from transactions.models import Wallet
from information.models import InformationForTransaction


class ModelsTest(TestCase):
    def setUp(self):
        self.user = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='test_create@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )
        self.wallet = Wallet.objects.create(
            owner=self.user,
            balance='111',
        )

    def test_InformationForTransaction_model(self):
        information = InformationForTransaction.objects.create(
            wallet=self.wallet,
            last_used_currency='CHF'
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
