from rest_framework import serializers
from .models import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        
class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'
     
class RolePriceSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    class Meta:
        model = RolePrice
        fields = '__all__'     

class SizeChartSerializer(serializers.ModelSerializer):
    price_map = serializers.SerializerMethodField()
    class Meta:
        model = SizeChart
        fields = ['id','disable','size','quantity','product','finish','price_map']  
        
    def get_price_map(self,obj):
        price_map = RolePrice.objects.filter(size=obj)
        return RolePriceSerializer(price_map,many=True).data

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        
class FinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finish
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    main_category = MainCategorySerializer()
    sub_category = SubCategorySerializer()
    size_chart = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name','description','image','stock_quantity','sku_code','disable','main_category','sub_category','size_chart']
        
    def get_size_chart(self,obj):
        size_chart = SizeChart.objects.filter(product=obj)
        return SizeChartSerializer(size_chart,many=True).data