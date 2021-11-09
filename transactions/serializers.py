from rest_framework import serializers
from .models import Transaction, Wallet
from decimal import Decimal, getcontext

from pprint import pprint

getcontext().prec = 2


class FillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value',)

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value',)

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value', 'email',)

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction


class TransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    type = serializers.CharField()
    value = serializers.DecimalField(max_digits=15, decimal_places=2)



