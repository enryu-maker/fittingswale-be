from rest_framework import serializers
from .models import *

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = "__all__"
        
class RefundCancellationPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundCancellationPolicy
        fields = "__all__"

class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = "__all__"