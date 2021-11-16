from rest_framework import serializers

from transactions.models import Wallet
from user.models import VirtualWalletUser


class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance',)
