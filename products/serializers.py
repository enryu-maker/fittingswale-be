from rest_framework import serializers
from .models import *

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
    
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        
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
        fields = ['id','status','size','quantity','product','finish','price_map']  
        
    def get_price_map(self,obj):
        price_map = RolePrice.objects.filter(size=obj)
        return RolePriceSerializer(price_map,many=True).data

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id','sub_category_name','image','status']
        
class FinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finish
        fields = '__all__'

class MultiImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiImages
        fields = "__all__"

class ProductImageSerializer(serializers.ModelSerializer):
    finish = FinishSerializer()
    images = serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = ['id','finish','status','images']
    
    def get_images(self,obj):
        return MultiImageSerializer(MultiImages.objects.filter(prod_img=obj),many=True).data      

class ProductSerializer(serializers.ModelSerializer):
    main_category = MainCategorySerializer()
    sub_category = SubCategorySerializer()
    product_images = serializers.SerializerMethodField()
    size_chart = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    product_details =serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name','description','image','stock_quantity','sku_code','status','main_category','sub_category','size_chart','product_images','product_details','location']
        
    def get_size_chart(self,obj):
        size_chart = SizeChart.objects.filter(product=obj)
        return SizeChartSerializer(size_chart,many=True).data
    
    def get_product_images(self,obj):
        images = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(images,many=True).data
    
    def get_location(self,obj):
        location = Location.objects.filter(product=obj)
        return LocationSerializer(location,many=True).data
    
    def get_product_details(self,obj):
        product = ProductDetail.objects.filter(product=obj)
        return ProductDetailSerializer(product,many=True).data
    

class MainCategoryWithSubCategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = MainCategory
        fields = ['category_name','image','status','sub_category']
    
    def get_sub_category(self,obj):
        sub_category = SubCategory.objects.filter(main_category=obj)
        return SubCategorySerializer(sub_category,many=True).data
    
class SubCategoryWithProductSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = SubCategory
        fields = ['sub_category_name','image','status','products']
    
    def get_products(self,obj):
        return ProductSerializer(Product.objects.filter(sub_category=obj),many=True).data
        