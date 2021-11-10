from django.shortcuts import render
from django.db.transaction import atomic
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from .serializers import FillSerializer, WithdrawSerializer, PaySerializer, TransactionSerializer
from .models import Transaction, Wallet


class FillWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FillSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(owner=request.user)
        transaction.save()
        return Response(data={'response': 'Successful fill'}, status=200)


class WithdrawWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WithdrawSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(owner=request.user)
        transaction.save()
        return Response(data={'response': 'Successful withdraw'}, status=200)


class PayWalletView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(data={'response': 'Successful payment'}, status=200)


class TransactionsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_wallet = Wallet.objects.get(owner=self.request.user)
        users_transactions = Transaction.objects.filter(
            wallet=user_wallet,
            date__lte=self.request.GET['start_date'],
            date__gte=self.request.GET['end_date']
        )
        return Transaction.objects.filter(id__in=users_transactions)

