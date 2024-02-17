from django.contrib import admin
from .models import Product,MainCategory,SizeChart,RolePrice,SubCategory,ProductImage,Role,Finish
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class SizeChartInline(admin.TabularInline):
    model = SizeChart
    extra = 1

class RolePriceInline(admin.TabularInline):
    model = RolePrice
    extra = 1

class ProductAdmin(admin.ModelAdmin):     
    inlines=[ProductImageInline,SizeChartInline,RolePriceInline]


admin.site.register(RolePrice)
admin.site.register(Product,ProductAdmin)
admin.site.register(MainCategory)
admin.site.register(Finish)
admin.site.register(Role)
admin.site.register(SizeChart)
admin.site.register(SubCategory)