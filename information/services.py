from currency_converter import CurrencyConverter
from decimal import Decimal


def convert_to_currency(value: float, currency_to_convert: str, default_currency='USD') -> Decimal:
    """
    Returns wallet balance converted to given currency.
    'UAH' isn't supported :(
    """
    converter = CurrencyConverter()
    return Decimal(converter.convert(value, default_currency, currency_to_convert)).\
        quantize(Decimal('.01'))
