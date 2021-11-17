from currency_converter import CurrencyConverter
from decimal import Decimal

from.validators import validate_currency_type


def convert_to_currency(value: float, currency_to_convert: str, default_currency='USD') -> Decimal:
    """
    Returns wallet balance converted to given currency
    """
    validate_currency_type(currency_to_convert)
    converter = CurrencyConverter()
    return Decimal(converter.convert(value, default_currency, currency_to_convert)).\
        quantize(Decimal('.01'))



