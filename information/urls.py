from django.urls import path

from . import views

urlpatterns = [
    path('balance/', views.ShowBalanceWithCurrency.as_view(), name='balance'),
    path('summary/', views.ShowSummaryForGivenPeriod.as_view(), name='summary'),
    path('series/', views.ShowAggregationForGivenPeriod.as_view(), name='series'),
]

