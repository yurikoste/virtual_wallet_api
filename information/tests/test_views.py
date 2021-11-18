from django.test import TestCase, Client
from rest_framework.test import force_authenticate, APIRequestFactory
from decimal import Decimal, getcontext
from collections import OrderedDict
from datetime import date, timedelta
from unittest.mock import patch

from user.models import VirtualWalletUser
from transactions.models import Wallet, Transaction
from information.views import ShowBalanceWithCurrency, ShowSummaryForGivenPeriod, ShowAggregationForGivenPeriod
from config.settings import DEFAULT_CURRENCY
from information.services import _get_conversion_rates


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
            balance=150
        )

        transaction = Transaction.objects.create(
            wallet=self.wallet,
            email='test_create@example.com',
            type='payment_received',
            value=100
        )

        transaction = Transaction.objects.create(
            wallet=self.wallet,
            email='test_create@example.com',
            type='payment_fill',
            value=50
        )

        transaction = Transaction.objects.create(
            wallet=self.wallet,
            email='test_create@example.com',
            type='payment_fill',
            value=5
        )

        transaction = Transaction.objects.create(
            wallet=self.wallet,
            email='test_create@example.com',
            type='payment_withdraw',
            value=200
        )

        transaction_yesterday = Transaction.objects.get(value=200)
        transaction_yesterday.date = str(date.today()-timedelta(days=1))
        transaction_yesterday.save(update_fields=['date'])

    # @patch('information.services._get_conversion_rates', return_value={'USD': 0.75, 'EUR': 1.00, 'CHF': 0.75})
    def test_show_balance_with_currency(self):
        factory = APIRequestFactory()
        view = ShowBalanceWithCurrency.as_view()
        request = factory.get('api/v1/information/balance?currency=USD')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_show_balance_with_default_currency_response(self):
        factory = APIRequestFactory()
        view = ShowBalanceWithCurrency.as_view()
        response_data = {'balance': Decimal('150.00')}
        request = factory.get(f'api/v1/information/balance?currency={DEFAULT_CURRENCY}')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def test_show_summary_for_period(self):
        factory = APIRequestFactory()
        view = ShowSummaryForGivenPeriod.as_view()
        request = factory.get(
            f'api/v1/information/summary?currency=CHF&start_date={date.today()}&end_date={date.today()}'
        )
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_show_summary_for_period_response(self):
        factory = APIRequestFactory()
        view = ShowSummaryForGivenPeriod.as_view()
        response_data = {
            'payment_received': Decimal('100.00'),
            'payment_fill': Decimal('55.00'),
            'payment_withdraw': Decimal('200.00')
        }
        request = factory.get(
            f'api/v1/information/summary?currency=EUR&start_date='
            f'{date.today()-timedelta(days=1)}&end_date={date.today()}'
        )
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)

    def test_show_aggregation_for_period(self):
        factory = APIRequestFactory()
        view = ShowAggregationForGivenPeriod.as_view()
        request = factory.get(
            f'api/v1/information/series?currency=CHF&start_date={date.today()}&end_date={date.today()}'
        )
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_show_aggregation_for_period_reponse(self):
        factory = APIRequestFactory()
        view = ShowAggregationForGivenPeriod.as_view()
        response_data = {
            'payment_received': [Decimal('0.00'), Decimal('100.00')],
            'payment_fill': [Decimal('0.00'), Decimal('55.00')],
            'payment_made': [Decimal('0.00'), Decimal('0.00')],
            'payment_withdraw': [Decimal('200.00'), Decimal('0.00')],
            'date': [str(date.today()-timedelta(days=1)), str(date.today())]
        }
        request = factory.get(
            f'api/v1/information/series?currency=EUR&start_date='
            f'{date.today()-timedelta(days=1)}&end_date={date.today()}'
        )
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)
