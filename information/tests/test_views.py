from decimal import Decimal
from collections import OrderedDict
from datetime import date, timedelta
from unittest.mock import patch

from django.test import TestCase, Client
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status

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

    @patch('information.services._get_conversion_rates', return_value={'USD': 0.75, 'EUR': 1.00, 'CHF': 0.75})
    def test_show_balance_with_currency(self, _get_conversion_rates):
        view = ShowBalanceWithCurrency.as_view()
        response = _setup_request_for_view_test_template(self, view, "api/v1/information/balance?currency=USD")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('information.services._get_conversion_rates', return_value={'USD': 0.5, 'EUR': 1.00, 'CHF': 0.75})
    def test_show_balance_with_default_currency_response(self, _get_conversion_rates):
        view = ShowBalanceWithCurrency.as_view()
        response_data = {'balance': Decimal('150.00')}
        response = _setup_request_for_view_test_template(self, view, "api/v1/information/balance?currency=EUR")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    @patch('information.services._get_conversion_rates', return_value={'USD': 0.75, 'EUR': 1.00, 'CHF': 0.75})
    def test_show_summary_for_period(self, _get_conversion_rates):
        view = ShowSummaryForGivenPeriod.as_view()
        response = _setup_request_for_view_test_template(
            self, view, f"api/v1/information/summary?currency=CHF&start_date={date.today()}&end_date={date.today()}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('information.services._get_conversion_rates', return_value={'USD': 0.5, 'EUR': 1.00, 'CHF': 0.75})
    def test_show_summary_for_period_response(self, _get_conversion_rates):
        view = ShowSummaryForGivenPeriod.as_view()
        response_data = {
            'payment_received': Decimal('50.00'),
            'payment_fill': Decimal('27.5'),
            'payment_withdraw': Decimal('100.00')
        }
        response = _setup_request_for_view_test_template(
            self, view, f"api/v1/information/summary?currency=USD&"
                        f"start_date={date.today()-timedelta(days=1)}&end_date={date.today()}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)

    @patch('information.services._get_conversion_rates', return_value={'USD': 0.75, 'EUR': 1.00, 'CHF': 0.75})
    def test_show_aggregation_for_period(self, _get_conversion_rates):
        view = ShowAggregationForGivenPeriod.as_view()
        response = _setup_request_for_view_test_template(
            self, view, f"api/v1/information/series?currency=CHF&start_date={date.today()}&end_date={date.today()}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('information.services._get_conversion_rates', return_value={'USD': 0.75, 'EUR': 1.00, 'CHF': 0.75})
    def test_show_aggregation_for_period_response(self, _get_conversion_rates):
        view = ShowAggregationForGivenPeriod.as_view()
        response_data = {
            'payment_received': [Decimal('0.00'), Decimal('75.00')],
            'payment_fill': [Decimal('0.00'), Decimal('41.25')],
            'payment_made': [Decimal('0.00'), Decimal('0.00')],
            'payment_withdraw': [Decimal('150.00'), Decimal('0.00')],
            'date': [str(date.today()-timedelta(days=1)), str(date.today())]
        }
        response = _setup_request_for_view_test_template(self, view,
                                                         f"api/v1/information/series?currency=CHF&"
                                                         f"start_date={date.today()-timedelta(days=1)}&"
                                                         f"end_date={date.today()}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_data)


def _setup_request_for_view_test_template(self, view, path_with_request: str):
    """

    :param self:
    :param view: View instance to test
    :param path_with_request: Path to endpoint with query parameters
    :return: Result of view(request)
    """
    factory = APIRequestFactory()
    request = factory.get(f'{path_with_request}')
    force_authenticate(request, user=self.user)
    return view(request)

