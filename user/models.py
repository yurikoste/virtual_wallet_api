from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class VirtualWalletUser(AbstractUser):
    # wallet_id = models.IntegerField()
    birth_date = models.DateField(blank=False, null=True, verbose_name='Birth date')

    def __str__(self):
        return f"{self.username}"

