from django.contrib import admin
from django.urls import path,include
from .views import *
from products.views import PaymentTransactionAPIView

urlpatterns = [
    path('login/', LoginUserAPIView.as_view()),
    path('',UserAPIView.as_view()),
    path('verify/',VerifyOTPAPIView.as_view()),
    path('forget-password/',ForgotPasswordAPIView.as_view()),
    path('reset-password/<str:uidb64>/<str:token>/',ResetPasswordAPIView.as_view()),
    path('register/',RegisterUserAPIView.as_view()),
    path('edit-profile/',EditUserAPIView.as_view()),
    path('google-login/',GoogleLoginAPIView.as_view()),
    path('address/<int:pk>/',UserAddressAPIView.as_view(),name="user_adress"),
    path('get-orders/',OrderAPIView.as_view(),name="get_orders"),
    path('paymenttransactions/', PaymentTransactionAPIView.as_view(), name='payment_transactions_api'),
]
