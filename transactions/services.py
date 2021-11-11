def convert_balance_to_currency(amount, currency):
    return amount*_currency_exchange_rate(currency)


def _currency_exchange_rate(currency):
    rates = {
        'UAH': 1,
        'USD': 25,
        'EUR': 30,
    }
    return rates[currency]


def _update_currency_exchange_rate():
    pass
