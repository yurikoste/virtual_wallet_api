from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from django.db.transaction import atomic
from django.core.exceptions import ObjectDoesNotExist

from decimal import Decimal, getcontext

from .serializers import FillSerializer, WithdrawSerializer, PaySerializer, TransactionSerializer
from .models import Transaction, Wallet
from user.models import VirtualWalletUser


from pprint import pprint
# class IsOwnerOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user

getcontext().prec = 2


class FillWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FillSerializer

    def post(self, request, *args, **kwargs):
        user = VirtualWalletUser.objects.get(id=request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(email=user.email, type='payment_fill', wallet=user.wallet)
        transaction.save()

        wallet = transaction.wallet
        wallet.balance += Decimal(
            FillSerializer(transaction, context=self.get_serializer_context()).data['value']
        )

        wallet.save()
        return Response(data={'response': 'Successful fill'}, status=200)
        # return Response({
        #     "Value": FillSerializer(transaction, context=self.get_serializer_context()).data['value'],
        # })


class WithdrawWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WithdrawSerializer

    def post(self, request, *args, **kwargs):
        user = VirtualWalletUser.objects.get(id=request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user.wallet.balance < Decimal(request.data['value']):
            return Response(data={'response': "Sorry, you don't have enough money in your wallet"}, status=200)
        else:
            transaction = serializer.save(email=user.email, type='payment_withdraw', wallet=user.wallet)
            transaction.save()
            # wallet = transaction.wallet

            user.wallet.balance -= Decimal(
                FillSerializer(transaction, context=self.get_serializer_context()).data['value']
            )
            user.wallet.save()
            return Response(data={'response': 'Successful withdraw'}, status=200)
        # return Response({
        #     "Value": FillSerializer(transaction, context=self.get_serializer_context()).data['value'],
        # })


class PayWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaySerializer

    def post(self, request, *args, **kwargs):
        user = VirtualWalletUser.objects.get(id=request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payer_wallet = user.wallet

        if payer_wallet.balance < Decimal(request.data['value']):
            return Response(data={'response': "Sorry, you don't have enough money in your wallet"}, status=200)
        else:
            try:
                receiver = VirtualWalletUser.objects.get(email=request.data['email'])
            except ObjectDoesNotExist:
                return Response(data={'response': "There is no receiver with such email"}, status=200)
            with atomic():
                payer_wallet.balance -= Decimal(request.data['value'])
                receiver_wallet = receiver.wallet
                receiver_wallet.balance += Decimal(request.data['value'])

                payer_wallet.save()
                receiver_wallet.save()

                payer_transaction = serializer.save(wallet=payer_wallet, type='payment_made')
                receiver_transaction = Transaction.objects.create(
                    wallet=receiver_wallet,
                    email=receiver_wallet.owner,
                    type='payment_received',
                    value=Decimal(request.data['value'])
                )

                return Response(data={'response': "Successful payment"}, status=200)


class TransactionsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_wallet = Wallet.objects.get(owner=self.request.user)
        pprint(f"{user_wallet=}")
        users_transactions = Transaction.objects.filter(
            wallet=user_wallet,
            date__lte=self.request.GET['start_date'],
            date__gte=self.request.GET['end_date']
        )
        return Transaction.objects.filter(id__in=users_transactions)

