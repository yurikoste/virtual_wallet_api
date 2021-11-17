from rest_framework import serializers
from django.db.models import Sum

from transactions.models import Wallet, Transaction
from user.models import VirtualWalletUser
from .services import convert_to_currency

from pprint import pprint


class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance',)


class ShowPeriodSummarySerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = ('value', 'type',)

    def save(self, **validated_data):
        user = VirtualWalletUser.objects.get(pk=validated_data['owner'].id)
        users_transactions = Transaction.objects.filter(
            wallet=user.wallet,
            date__gte=validated_data['start_date'],
            date__lte=validated_data['end_date']
        )

        data = {}
        for operation_type in Transaction.types:
            transactions_sum = users_transactions.filter(type=operation_type[0]).aggregate(Sum('value'))
            if transactions_sum['value__sum']:
                data[operation_type[0]] = convert_to_currency(
                    value=transactions_sum['value__sum'],
                    currency_to_convert=validated_data['currency'],
                    default_currency='EUR'
                )
        return data
