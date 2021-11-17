from datetime import datetime, timedelta
from decimal import Decimal, getcontext

from rest_framework import serializers
from django.db.models import Sum

from transactions.models import Wallet, Transaction
from user.models import VirtualWalletUser
from .services import convert_to_currency
from .validators import SUPPORTED_CURRENCIES, validate_start_and_end_dates
from .models import InformationForTransaction

from pprint import pprint
from django.db import connection


class WalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationForTransaction
        fields = ('last_used_currency',)

    def save(self, **validated_data):
        user = VirtualWalletUser.objects.get(pk=validated_data['owner'].id)
        information, created = InformationForTransaction.objects.get_or_create(wallet_id=user.wallet.pk)
        information.last_used_currency = validated_data['currency']
        information.save(update_fields=['last_used_currency'])

        data = {'balance': convert_to_currency(
            value=user.wallet.balance,
            currency_to_convert=validated_data['currency'],
            default_currency='EUR'
        )}
        return data


class PeriodSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationForTransaction
        fields = ('last_used_currency',)

    def create(self, **validated_data):
        validate_start_and_end_dates(validated_data['start_date'], validated_data['end_date'])
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


class PeriodAggregateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationForTransaction
        fields = ('last_used_currency',)

    def create(self, **validated_data):
        validate_start_and_end_dates(validated_data['start_date'], validated_data['end_date'])
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

        for day in dates:
            day_transactions = Transaction.objects.filter(date=day)
            if day_transactions:
                for operation_type in Transaction.types:
                    transactions_sum = day_transactions.filter(type=operation_type[0]).aggregate(Sum('value'))
                    if transactions_sum['value__sum']:
                        data[operation_type[0]].append(convert_to_currency(
                            value=transactions_sum['value__sum'],
                            currency_to_convert=validated_data['currency'],
                            default_currency='EUR',
                        ))
                    else:
                        data[operation_type[0]].append(Decimal(0))
                data['date'].append(day)
            else:
                for operation_type in Transaction.types:
                    data[operation_type[0]].append(Decimal(0))
                data['date'].append(day)
        return data
