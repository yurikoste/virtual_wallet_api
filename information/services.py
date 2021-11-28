from decimal import Decimal
import requests
from django.core.cache import cache as cache
from config.settings import EXCHANGE_API_URL, EXCHANGE_API_KEY

from.validators import validate_currency_type


def convert_to_currency(value: Decimal, currency_to_convert: str) -> Decimal:
    """
    Returns wallet balance converted to a given currency
    """
    rates = _get_conversion_rates()
    validate_currency_type(currency_to_convert)
    return (value*Decimal(rates[currency_to_convert])).quantize(Decimal('.01'))


def _get_conversion_rates() -> dict:
    """
    Get conversion rate from exchange rate API
    :return: dictionary with currency rates
    """
    if rates := cache.get('rates'):
        return rates
    else:
        request_results = requests.get(f"{EXCHANGE_API_URL}access_key={EXCHANGE_API_KEY}").json()
        cache.set('rates', request_results['rates'])
        return request_results['rates']





