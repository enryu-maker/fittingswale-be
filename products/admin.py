from django.contrib import admin
from .models import *
from django import forms
from nested_admin import NestedTabularInline, NestedModelAdmin
    
class MulitiImageInline(NestedTabularInline):
    model = MultiImages
    extra = 0
    classes = ('collapse',)
 
class ProductImageInline(NestedTabularInline):
    model = ProductImage
    extra = 1
    classes = ('collapse', )
    inlines = [MulitiImageInline]

class ProductDetailInline(NestedTabularInline):
    model = ProductDetail
    extra = 1
    classes = ('collapse', )

class RolePriceInline(NestedTabularInline):
    model = RolePrice
    extra = 1
    classes = ('collapse', )
    
class SizeChartInline(NestedTabularInline):
    model = SizeChart
    extra = 1
    inlines = [RolePriceInline,]
    classes = ('collapse', )
    
class LocationInline(NestedTabularInline):
    model = Location
    extra = 1
    classes = ('collapse', )

class MainCategoryAdmin(admin.ModelAdmin):
    list_display=['category_name','status']

class SubCategoryAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display=['sub_category_name','main_category','status']

class SizeChartAdmin(admin.ModelAdmin):
    inlines =[RolePriceInline,]

class ProductAdmin(NestedModelAdmin):     
    search_fields = ['product_name']
    list_filter = ['status','main_category']
    list_display=['id','product_name','main_category','sub_category','stock_quantity','status']
    inlines=[ProductImageInline,ProductDetailInline,SizeChartInline,LocationInline]

admin.site.register(RolePrice)
admin.site.register(Product,ProductAdmin)
admin.site.register(MainCategory,MainCategoryAdmin)
admin.site.register(Finish)
admin.site.register(Role)
admin.site.register(SizeChart,SizeChartAdmin)
admin.site.register(Location)
admin.site.register(MultiImages)
admin.site.register(ProductImage)
admin.site.register(SubCategory,SubCategoryAdmin)