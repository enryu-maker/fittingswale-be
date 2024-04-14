from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BestSellerProduct, SpotlightProduct
from .serializers import *

class BestSellerProductList(APIView):
    def get(self, request, format=None):
        bestsellers = BestSellerProduct.objects.all()
        serializer = BestSellerProductSerializer(bestsellers, many=True)
        return Response(serializer.data)

class SpotlightProductList(APIView):
    def get(self, request, format=None):
        spotlights = SpotlightProduct.objects.all()
        serializer = SpotlightProductSerializer(spotlights, many=True)
        return Response(serializer.data)
