from information.models import InformationForTransaction
from rest_framework import serializers

SUPPORTED_CURRENCIES = [currency[0] for currency in InformationForTransaction.currency_types]


def validate_currency_type(currency: str) -> None:
    """
    Check if currency is in the list of supported currencies
    :param currency: Currency to validate
    :return:
    """
    if currency not in SUPPORTED_CURRENCIES:
        raise serializers.ValidationError("Unsupported currency type")


def validate_start_and_end_dates(start_date: str, end_date: str) -> None:
    """
    Check if end date if later or in the same day as start day
    :param start_date: Start date of the given period
    :param end_date: End date of the given period
    :return:
    """
    if start_date > end_date:
        raise serializers.ValidationError("End date must occur after start date")
