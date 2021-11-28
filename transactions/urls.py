from django.urls import path

from . import views

urlpatterns = [
    path('fill/', views.FillWalletView.as_view(), name='fill'),
    path('withdraw/', views.WithdrawWalletView.as_view(), name='withdraw'),
    path('pay/', views.PayWalletView.as_view(), name='pay'),
    path('', views.TransactionsView.as_view(), name='details')
]
