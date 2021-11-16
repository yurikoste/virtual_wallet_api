from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from transactions.models import Wallet
from .serializers import WalletBalanceSerializer
from .services import convert_to_currency


class ShowBalanceWithCurrency(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletBalanceSerializer
    queryset = Wallet.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        wallet = queryset.get(pk=self.request.user.pk)
        wallet.balance = convert_to_currency(
            value=wallet.balance,
            currency_to_convert=self.request.GET['currency'],
            default_currency='EUR'
            )
        return wallet
