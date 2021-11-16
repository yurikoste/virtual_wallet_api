from django.urls import path

from . import views

urlpatterns = [
    path('balance/', views.ShowBalanceWithCurrency.as_view(), name='balance'),
]

