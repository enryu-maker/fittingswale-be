from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"privacy-policy",PricvacyPolicyViewSet,basename='privacy-policy')
router.register(r"terms-and-conditions",TermsAndCondtionViewSet,basename='terms-and-conditions')
router.register(r"refund-cancellation-policy",RefundCancellationViewSet,basename='return-cancellation-policy')

urlpatterns = [
    path('',include(router.urls)),
    path('data/',AddData.as_view()),
]
