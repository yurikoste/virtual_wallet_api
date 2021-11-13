from django.test import TestCase, Client
from rest_framework.test import force_authenticate, APIRequestFactory

from user.models import VirtualWalletUser
from transactions.models import Wallet
from transactions.views import FillWalletView, WithdrawWalletView, PayWalletView

from pprint import pprint


class ViewsTesting(TestCase):
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
            balance='100',
            last_used_currency='UAH'
        )

        self.client = Client()

    def test_fill_without_auth(self):
        _fill_view_test_template(self=self,
                                 value='100',
                                 endpoint="/api/v1/transactions/fill/",
                                 user=self.user,
                                 is_authenticated=False,
                                 response_code=403
                                 )

    def test_fill_zero(self):
        _fill_view_test_template(self=self,
                                 value='0',
                                 endpoint="/api/v1/transactions/fill/",
                                 user=self.user,
                                 is_authenticated=True,
                                 response_code=400
                                 )

    def test_fill(self):
        _fill_view_test_template(self=self,
                                 value='100',
                                 endpoint="/api/v1/transactions/fill/",
                                 user=self.user,
                                 is_authenticated=True,
                                 response_code=200
                                 )

    def test_withdraw_without_auth(self):
        _withdraw_view_test_template(self=self,
                                     value='100',
                                     endpoint="/api/v1/transactions/withdraw/",
                                     user=self.user,
                                     is_authenticated=False,
                                     response_code=403)

    def test_withdraw_zero(self):
        _withdraw_view_test_template(self=self,
                                     value='0',
                                     endpoint="/api/v1/transactions/withdraw/",
                                     user=self.user,
                                     is_authenticated=True,
                                     response_code=400)

    def test_withdraw_too_many(self):
        _withdraw_view_test_template(self=self,
                                     value=1e30,
                                     # value='10000000',
                                     endpoint="/api/v1/transactions/withdraw/",
                                     user=self.user,
                                     is_authenticated=True,
                                     response_code=400)

    def test_withdraw(self):
        _withdraw_view_test_template(self=self,
                                     value='1',
                                     endpoint="/api/v1/transactions/withdraw/",
                                     user=self.user,
                                     is_authenticated=True,
                                     response_code=200)

    def test_pay_view(self):
        factory = APIRequestFactory()
        view = PayWalletView.as_view()

        receiver = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='receiver@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )

        receiver_wallet = Wallet.objects.create(
            owner=receiver,
            balance='100',
            last_used_currency='UAH'
        )

        data = {
            'value': '1',
            'email': 'receiver@example.com'
        }

        request = factory.post('/api/v1/transactions/pay/', data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
            self.user = VirtualWalletUser.objects.create(
                password='aA987654321',
                email='test_delete@example.com',
                first_name='User',
                last_name='Test',
                birth_date='1987-08-30'
            )
            self.user.delete()


def _fill_and_withdraw_common_call(self, view, value, user, endpoint, is_authenticated, response_code):
    factory = APIRequestFactory()

    data = {
        'value': value
    }

    request = factory.post(endpoint, data)
    if is_authenticated:
        force_authenticate(request, user=user)
    response = view(request)
    self.assertEqual(response.status_code, response_code)


def _fill_view_test_template(self, value, user, endpoint, is_authenticated, response_code):
    view = FillWalletView.as_view()
    _fill_and_withdraw_common_call(self, view, value, user, endpoint, is_authenticated, response_code)


def _withdraw_view_test_template(self, value, user, endpoint, is_authenticated, response_code):
    view = WithdrawWalletView.as_view()
    _fill_and_withdraw_common_call(self, view, value, user, endpoint, is_authenticated, response_code)
