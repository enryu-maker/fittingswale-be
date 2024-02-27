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
        
class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id','category_name','status','sub_category']
        
    def get_sub_category(self,obj):
        return SubCategorySerializer(SubCategory.objects.filter(category=obj),many=True).data
        
class MainCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    class Meta:
        model = MainCategory
        fields = ['id','main_category_name','image','status','category']
        
    def get_category(self,obj):
        return CategorySerializer(Category.objects.filter(main_category=obj),many=True).data
     
class RolePriceSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    class Meta:
        model = RolePrice
        fields = '__all__'     

class SizeChartSerializer(serializers.ModelSerializer):
    price_map = serializers.SerializerMethodField()
    class Meta:
        model = SizeChart
        fields = ['id','status','size','quantity','finish','price_map']  
        
    def get_price_map(self,obj):
        role_id = 1 if self.context.get('role_id') is None else self.context.get('role_id')
        try:
            role = Role.objects.get(pk=role_id)
        except:
            role = Role.objects.get(pk=1)
        price_map = RolePrice.objects.filter(size=obj,role=role)
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
    product_images = serializers.SerializerMethodField()
    size_chart = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    product_details =serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name','description','image','sku_code','status','size_chart','product_images','product_details','location']
        
    def get_size_chart(self,obj):
        role_id = self.context.get('role_id')
        size_chart = SizeChart.objects.filter(product=obj)
        return SizeChartSerializer(size_chart,many=True,context={'role_id': role_id}).data
    
    def get_product_images(self,obj):
        images = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(images,many=True).data
    
    def get_location(self,obj):
        location = Location.objects.filter(product=obj)
        return LocationSerializer(location,many=True).data
    
    def get_product_details(self,obj):
        product = ProductDetail.objects.filter(product=obj)
        return ProductDetailSerializer(product,many=True).data

class SubCategoryProductSerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = SubCategory
        fields = ['id','sub_category_name','image','products']
        
    def get_products(self,obj):
        role_id = self.context.get('role_id')
        return ProductSerializer(Product.objects.filter(sub_category=obj),many=True,context={'role_id': role_id}).data