from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
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
    
class AddData(APIView):
    def post(self,request):
        data = request.data
        for i in data:
            serializer = TermsAndConditionSerializer(data=i)
            if serializer.is_valid():
                serializer.save()
        return Response({'msg':'done'})
    
class BannerAPIView(APIView):
    def get(self,request):
        banner = Banner.objects.all()
        serializer = BannerSerializer(banner,many=True)
        return Response(serializer.data)