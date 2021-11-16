from currency_converter import CurrencyConverter
from decimal import Decimal


def convert_to_currency(value: float, currency_to_convert: str, default_currency='UAH') -> Decimal:
    """
    Returns wallet balance converted to given currency
    """
    converter = CurrencyConverter(decimal=True)
    return converter.convert(value, default_currency, currency_to_convert)
