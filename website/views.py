
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BestSellerProduct, SpotlightProduct
from .serializers import *
from rest_framework.generics import ListAPIView
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

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

class NewProductAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        role_id = 1
        if request.user.is_authenticated:
            if request.user.role == "Business":
                role_id=3
            elif request.user.role == "Interior":
                role_id=2
        try:
            newest_products = Product.objects.order_by('-id')[:8]
            serializer = ProductSerializer(newest_products,context={'role_id': role_id},many=True)
            return Response(serializer.data)
        except:
            return Response({'msg':'product not found'},status=status.HTTP_404_NOT_FOUND)
    

