from django.db import models
from transactions.models import Wallet

CURRENCY_TYPES = (
    ('EUR', 'EUR'),
    ('CHF', 'CHF'),
    ('USD', 'USD'),
)


class InformationForTransaction(models.Model):
    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, related_name="information", verbose_name='Information'
    )
    last_used_currency = models.CharField(choices=CURRENCY_TYPES, default='EUR', max_length=3)

    def __str__(self):
        return f"Currency used for requests is {self.last_used_currency}"
