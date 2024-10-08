from django.contrib import admin
from django.urls import path, include
from .views import *
from products.views import PaymentTransactionAPIView, PayUTransactionAPIView
from .razor_pay_views import RazorpayOrderAPIView, TransactionAPIView
from .payu_views import PayUOrderAPIView

urlpatterns = [
    path('login/', LoginUserAPIView.as_view()),
    path('', UserAPIView.as_view()),
    path('verify/', VerifyOTPAPIView.as_view()),
    path('forget-password/', ForgotPasswordAPIView.as_view()),
    path('reset-password/<str:uidb64>/<str:token>/',
         ResetPasswordAPIView.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('edit-profile/', EditUserAPIView.as_view()),
    path('google-login/', GoogleLoginAPIView.as_view()),
    path('address/', UserAddressAPIView.as_view(), name="user_adress"),
    path('address/<int:pk>/', AddressAPIView.as_view(), name="user_single_adress"),
    path('get-active-address/', GetActiveAddressAPIView.as_view(),
         name="get_active_address"),
    path('set-active-address/<int:pk>/',
         AddressAPIView.as_view(), name="set_active_address"),
    path('get-orders/', OrderAPIView.as_view(), name="get_orders"),
    path('paymenttransactions/', PaymentTransactionAPIView.as_view(),
         name='payment_transactions_api'),
    path('create-order/', RazorpayOrderAPIView.as_view(), name='create_order'),
    path('verify-order/', PayUTransactionAPIView.as_view(), name='verify_order'),
    path("create-hash/", PayUOrderAPIView.as_view())
]
