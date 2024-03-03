from django.contrib import admin
from .models import *
from django import forms
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.utils.html import format_html    

class MulitiImageInline(NestedTabularInline):
    model = MultiImages
    extra = 0
    classes = ('collapse',)
    min_num = 1
 
class ProductImageInline(NestedTabularInline):
    model = ProductImage
    extra = 0
    classes = ('collapse', )
    inlines = [MulitiImageInline]
    min_num = 1

class ProductDetailInline(NestedTabularInline):
    model = ProductDetail
    extra = 0
    classes = ('collapse', )
    min_num = 1

class RolePriceInline(NestedTabularInline):
    model = RolePrice
    extra = 0
    classes = ('collapse', )
    min_num = 1
    
    
class LocationInline(NestedTabularInline):
    model = Location
    extra = 0
    classes = ('collapse', )
    min_num = 1
    
class SizeChartInline(NestedTabularInline):
    model = SizeChart
    extra = 0
    inlines = [RolePriceInline,LocationInline]
    classes = ('collapse', )
    min_num = 1

class MainCategoryAdmin(admin.ModelAdmin):
    def colored_status(self, obj):
        colors = {
            'Activate': 'green',
            'Inactivate': 'red',
        }
        return format_html(
            '<span style="background-color:{}; padding: 3px; border-radius: 3px; color: white;">{}</span>',
            colors[obj.status],
            obj.status,
        )
    colored_status.short_description = 'Status'
    list_display=['main_category_name','colored_status']

class SubCategoryAdmin(admin.ModelAdmin):
    list_filter = ['status']
    def colored_status(self, obj):
        colors = {
            'Activate': 'green',
            'Inactivate': 'red',
        }
        return format_html(
            '<span style="background-color:{}; padding: 3px; border-radius: 3px; color: white;">{}</span>',
            colors[obj.status],
            obj.status,
        )
    colored_status.short_description = 'Status'
    list_display=['sub_category_name','category','colored_status']

class SizeChartAdmin(admin.ModelAdmin):
    inlines =[RolePriceInline,LocationInline]

class CategoryAdmin(admin.ModelAdmin):
    def colored_status(self, obj):
        colors = {
            'Activate': 'green',
            'Inactivate': 'red',
        }
        return format_html(
            '<span style="background-color:{}; padding: 3px; border-radius: 3px; color: white;">{}</span>',
            colors[obj.status],
            obj.status,
        )
    colored_status.short_description = 'Status'
    list_display = ['category_name','colored_status']

class ProductAdmin(NestedModelAdmin):     
    
    def colored_status(self, obj):
        colors = {
            'Activate': 'green',
            'Inactivate': 'red',
        }
        return format_html(
            '<span style="background-color:{}; padding: 3px; border-radius: 3px; color: white;">{}</span>',
            colors[obj.status],
            obj.status,
        )
    colored_status.short_description = 'Status'
    
    search_fields = ['product_name']
    list_filter = ['status','main_category']
    list_display=['id','product_name','main_category','sub_category','colored_status']
    inlines=[ProductImageInline,ProductDetailInline,SizeChartInline]
    
class StockAdmin(admin.ModelAdmin):
    list_display= ['size_chart','minimum_quantity','stock_quantity']
    
    
class RolePriceAdmin(admin.ModelAdmin):    
    list_display = ['role','size','gst_percent','price_with_gst']



admin.site.register(RolePrice,RolePriceAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(MainCategory,MainCategoryAdmin)
admin.site.register(Finish)
admin.site.register(Role)
admin.site.register(SizeChart,SizeChartAdmin)
admin.site.register(Location)
admin.site.register(MultiImages)
admin.site.register(ProductImage)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(PaymentTransaction)
admin.site.register(Stock,StockAdmin)