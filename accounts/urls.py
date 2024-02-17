from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    # path('login/', admin.site.urls),
    # path('register/',include('accounts.urls')),
    # path('verify/<str:id>/<str:token>/',include('accounts.urls')),
    # path('forget-password/',include('accounts.urls')),
    # path('reset-password/',include('accounts.urls')),
    path('register/',RegisterUserAPIView.as_view())
]
