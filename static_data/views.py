from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *
# Create your views here.

class PricvacyPolicyViewSet(ModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer

class RefundCancellationViewSet(ModelViewSet):
    queryset = RefundCancellationPolicy.objects.all()
    serializer_class = RefundCancellationPolicySerializer

class TermsAndCondtionViewSet(ModelViewSet):
    queryset = TermsAndCondition.objects.all()
    serializer_class = TermsAndConditionSerializer