from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

]
