from datetime import datetime, timedelta
from decimal import Decimal, getcontext

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


class PeriodSummarySerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = ('value', 'type',)

    def create(self, **validated_data):
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


class PeriodAggregateSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = ('value', 'type',)

    def create(self, **validated_data):
        user = VirtualWalletUser.objects.get(pk=validated_data['owner'].id)
        users_transactions = Transaction.objects.filter(
            wallet=user.wallet,
            date__gte=validated_data['start_date'],
            date__lte=validated_data['end_date']
        )

        start_date = datetime.fromisoformat(validated_data['start_date'])
        end_date = datetime.fromisoformat(validated_data['end_date'])
        num_of_days = end_date - start_date
        dates = [str(start_date + timedelta(days=i)).split(' ')[0] for i in range(num_of_days.days + 1)]

        data = {operation_type[0]: [] for operation_type in Transaction.types}
        data['date'] = []

        pprint(f"{data=}")
        for day in dates:
            day_transactions = Transaction.objects.filter(date=day)
            if day_transactions:
                for operation_type in Transaction.types:
                    transactions_sum = day_transactions.filter(type=operation_type[0]).aggregate(Sum('value'))
                    if transactions_sum['value__sum']:
                        data[operation_type[0]].append(convert_to_currency(
                            value=transactions_sum['value__sum'],
                            currency_to_convert=validated_data['currency'],
                        ))
                    else:
                        data[operation_type[0]].append(Decimal(0))
                data['date'].append(day)
            else:
                for operation_type in Transaction.types:
                    data[operation_type[0]].append(Decimal(0))
                data['date'].append(day)
        return data
