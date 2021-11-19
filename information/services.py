from decimal import Decimal
import requests
from django.core.cache import cache as cache
from config.settings import EXCHANGE_API_URL, EXCHANGE_API_KEY, DEFAULT_CURRENCY

from.validators import validate_currency_type


def convert_to_currency(value: Decimal, currency_to_convert: str, default_currency=DEFAULT_CURRENCY) -> Decimal:
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
    if cache.get('rates'):
        return cache.get('rates')
    else:
        exchange_api_url = EXCHANGE_API_URL
        exchange_api_key = EXCHANGE_API_KEY
        url = f"http://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGE_API_KEY}"
        request_results = requests.get(url).json()
        cache.set('rates', request_results['rates'])
        return request_results['rates']





