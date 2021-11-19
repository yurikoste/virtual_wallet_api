from django.test import TestCase
from unittest.mock import patch
from decimal import Decimal
from information.services import _get_conversion_rates, convert_to_currency


class ServicesTesting(TestCase):
    @patch('information.services._get_conversion_rates', return_value={'USD': 0.75, 'EUR': 1.00, 'CHF': 0.75})
    def test_convert_to_currency(self, _get_conversion_rates):
        value_to_convert = Decimal('100.00')
        self.assertEqual(convert_to_currency(value_to_convert, 'USD', 'EUR'), Decimal('75.00'))




