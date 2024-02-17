from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/', LoginUserAPIView.as_view()),
    # path('register/',include('accounts.urls')),
    path('verify/',VerifyOTPAPIView.as_view()),
    path('forget-password/',ForgotPasswordAPIView.as_view()),
    path('reset-password/<str:uidb64>/<str:token>/',ResetPasswordAPIView.as_view()),
    path('register/',RegisterUserAPIView.as_view())
]
