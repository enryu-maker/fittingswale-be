# forms.py
from django import forms
from .models import Product, ProductImage, MultiImages

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['status', 'product', 'finish']  # Update fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['product'].widget.attrs['class'] = 'form-control'
        self.fields['finish'].widget.attrs['class'] = 'form-control'

class MultiImageForm(forms.ModelForm):
    class Meta:
        model = MultiImages
        fields = ['image', 'prod_img']  # Update fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['prod_img'].widget.attrs['class'] = 'form-control'
