from rest_framework import serializers
from .models import BestSellerProduct, SpotlightProduct
from products.serializers import ProductSerializer



class BestSellerProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = BestSellerProduct
        fields = '__all__'

class SpotlightProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SpotlightProduct
        fields = '__all__'
