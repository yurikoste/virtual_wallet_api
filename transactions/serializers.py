from django.db.transaction import atomic
from django.db.models import F
from rest_framework import serializers

from decimal import Decimal

from .models import Transaction
from user.models import VirtualWalletUser


class FillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value',)

    def create(self, **validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    def save(self, **validated_data):
        with atomic():
            user = VirtualWalletUser.objects.get(pk=validated_data['owner'].id)
            wallet = user.wallet
            wallet.balance = F('balance') + Decimal(self.initial_data['value'])
            wallet.save(update_fields=['balance'])
            transaction = Transaction.objects.create(wallet=wallet,
                                                     email=user.email,
                                                     type='payment_fill',
                                                     value=Decimal(self.initial_data['value']))
            return transaction

    @staticmethod
    def validate_value(value):
        if Decimal(value) <= 0:
            raise serializers.ValidationError("You have to fill wallet with amount bigger then 0")


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value',)

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    def save(self, **validated_data):
        with atomic():
            user = VirtualWalletUser.objects.get(pk=validated_data['owner'].id)
            wallet = user.wallet
            if wallet.balance < Decimal(self.initial_data['value']):
                raise serializers.ValidationError("Sorry, you don't have enough money in your wallet")
            wallet.balance = F('balance') - Decimal(self.initial_data['value'])
            wallet.save(update_fields=['balance'])
            transaction = Transaction.objects.create(wallet=wallet,
                                                     email=user.email,
                                                     type='payment_withdraw',
                                                     value=Decimal(self.initial_data['value']))
            return transaction

    @staticmethod
    def validate_value(value):
        if Decimal(value) <= 0:
            raise serializers.ValidationError("You have to withdraw with amount bigger then 0")


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('value', 'email',)

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

    def save(self, **validated_data):
        payer = VirtualWalletUser.objects.get(pk=validated_data['owner'].id)
        wallet = payer.wallet
        if wallet.balance < Decimal(self.initial_data['value']):
            raise serializers.ValidationError("Sorry, you don't have enough money in your wallet")
        else:
            with atomic():
                payer_wallet = payer.wallet
                receiver = VirtualWalletUser.objects.get(email=self.initial_data['email'])
                receiver_wallet = receiver.wallet

                payer_wallet.balance = F('balance') - Decimal(self.initial_data['value'])
                receiver_wallet.balance = F('balance') + Decimal(self.initial_data['value'])

                payer_wallet.save(update_fields=['balance'])
                receiver_wallet.save(update_fields=['balance'])

                payer_transaction = Transaction.objects.create(
                    wallet=payer_wallet,
                    email=payer.email,
                    type='payment_made',
                    value=Decimal(self.initial_data['value'])
                )

                receiver_transaction = Transaction.objects.create(
                    wallet=receiver_wallet,
                    email=receiver.email,
                    type='payment_received',
                    value=Decimal(self.initial_data['value'])
                )

                payer_transaction.save()
                receiver_transaction.save()

    @staticmethod
    def validate_value(value):
        if Decimal(value) <= 0:
            raise serializers.ValidationError("You have to define payment value bigger then 0")

    def validate_email(self, email):
        if not VirtualWalletUser.objects.filter(email=email):
            raise serializers.ValidationError("There is no payment receiver with such email. Please, check it")
        if email == self.context['request'].user.email:
            raise serializers.ValidationError("You can not pay to yourself. "
                                              "Use 'Fill' operation to put money on your wallet")


class TransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    type = serializers.CharField()
    value = serializers.DecimalField(max_digits=15, decimal_places=2)
