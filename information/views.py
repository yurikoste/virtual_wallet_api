from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import WalletBalanceSerializer, PeriodSummarySerializer, PeriodAggregateSerializer


class ShowBalanceWithCurrency(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletBalanceSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save(
            owner=request.user,
            currency=self.request.GET['currency'],
        )
        return Response(data=data, status=status.HTTP_200_OK)


class ShowSummaryForGivenPeriod(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PeriodSummarySerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(
            owner=request.user,
            start_date=self.request.GET['start_date'],
            end_date=self.request.GET['end_date'],
            currency=self.request.GET['currency'],
        )
        return Response(data=data, status=status.HTTP_200_OK)


class ShowAggregationForGivenPeriod(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PeriodAggregateSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(
            owner=request.user,
            start_date=self.request.GET['start_date'],
            end_date=self.request.GET['end_date'],
            currency=self.request.GET['currency'],
        )
        return Response(data=data, status=status.HTTP_200_OK)
