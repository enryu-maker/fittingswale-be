from django.contrib import admin
from .models import *
from django import forms
from nested_admin import NestedTabularInline, NestedModelAdmin
# Register your models here.

class ProductImageInline(NestedTabularInline):
    model = ProductImage
    extra = 1

class RolePriceInline(NestedTabularInline):
    model = RolePrice
    extra = 1
    
class SizeChartInline(NestedTabularInline):
    model = SizeChart
    extra = 1
    inlines = [RolePriceInline,]
    
class LocationInline(NestedTabularInline):
    model = Location
    extra = 1
    
class SizeChartAdmin(admin.ModelAdmin):
    inlines =[RolePriceInline,]

class ProductAdmin(NestedModelAdmin):     
    search_fields = ['product_name']
    list_filter = ['disable','main_category']
    list_display=['id','product_name','main_category','sub_category','stock_quantity','disable']
    inlines=[ProductImageInline,SizeChartInline,LocationInline]

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultiImageForm(forms.ModelForm):
    image = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = MultiImages
        fields = ['image']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('image'):
            for image in self.cleaned_data.get('image'):
                instance = MultiImages.objects.create(image=image)
        if commit:
            instance.save()
        return instance

class MultiImageAdmin(admin.ModelAdmin):
    form = MultiImageForm

admin.site.register(RolePrice)
admin.site.register(Product,ProductAdmin)
admin.site.register(MainCategory)
admin.site.register(Finish)
admin.site.register(Role)
admin.site.register(SizeChart,SizeChartAdmin)
admin.site.register(Location)
admin.site.register(MultiImages,MultiImageAdmin)
admin.site.register(ProductImage)
admin.site.register(SubCategory)