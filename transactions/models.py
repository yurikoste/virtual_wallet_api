from django.db import models
from user.models import VirtualWalletUser


class Wallet(models.Model):
    owner = models.OneToOneField(
        VirtualWalletUser, on_delete=models.CASCADE, related_name="wallet", verbose_name='Wallet'
    )
    balance = models.DecimalField(default=0, max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Wallet of {self.owner} with {self.balance}"


class Transaction(models.Model):
    types = (
        ('payment_received', 'payment_received'),
        ('payment_made', 'payment_made'),
        ('payment_withdraw', 'payment_withdraw'),
        ('payment_fill', 'payment_fill')
    )

    wallet = models.ForeignKey(
        Wallet, related_name='transactions', on_delete=models.CASCADE, verbose_name='Wallet'
    )

    email = models.CharField(max_length=128, blank=False, null=False)
    type = models.CharField(max_length=64, choices=types, default='payment_made')
    date = models.DateField(auto_now_add=True, verbose_name='Dates')
    value = models.DecimalField(default=0, max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.type} by {self.wallet.owner.email} in amount {self.value} to {self.email} on {self.date}"

