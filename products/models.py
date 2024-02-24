from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
# Create your models here.

from django.db.models.signals import pre_save
from django.dispatch import receiver



class Finish(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class MainCategory(models.Model):
    image = models.ImageField(upload_to='category', null=True, blank=True)
    category_name = models.CharField(max_length=255)
    DISABLE_CHOICES = [
        ('Activate', 'Activate'),
        ('Inactivate', 'Inactivate'),
    ]
    status = models.CharField(max_length=10, choices=DISABLE_CHOICES, default='Activate')


    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='subcategory', null=True, blank=True)
    DISABLE_CHOICES = [
        ('Activate', 'Activate'),
        ('Inactivate', 'Inactivate'),
    ]
    status = models.CharField(max_length=10, choices=DISABLE_CHOICES, default='Activate')


    def __str__(self):
        return self.sub_category_name

class Role(models.Model):
    title = models.CharField(_("Title"), max_length=10)
    def __str__(self):
        return self.title

class SizeChart(models.Model):
    DISABLE_CHOICES = [
        ('Activate', 'Activate'),
        ('Inactivate', 'Inactivate'),
    ]
    status = models.CharField(max_length=10, choices=DISABLE_CHOICES, default='Activate')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True)
    finish = models.ForeignKey(Finish,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"{self.product.product_name} - {self.size}"

class RolePrice(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeChart, on_delete=models.CASCADE,null=True,blank=True)
    gst_percent = models.DecimalField(max_digits=20, decimal_places=2,default=18,null=True)
    price_with_gst = models.DecimalField(max_digits=20,decimal_places=2,null=True)

    def __str__(self):
        return f"{self.role.title} - {self.price_with_gst}"

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product', null=True, blank=True)
    stock_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    minimum_quantity = models.IntegerField(validators=[MinValueValidator(0)],null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sku_code = models.CharField(max_length=30,null=True,blank=True)
    DISABLE_CHOICES = [
        ('Activate', 'Activate'),
        ('Inactivate', 'Inactivate'),
    ]
    status = models.CharField(max_length=10, choices=DISABLE_CHOICES, default='Activate')

    def __str__(self):
        return self.product_name

class MultiImages(models.Model):
    image = models.ImageField(upload_to="product_multi_images")
    prod_img = models.ForeignKey("ProductImage", verbose_name=_("Product Image"), on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.image.name

class ProductImage(models.Model):
    DISABLE_CHOICES = [
        ('Activate', 'Activate'),
        ('Inactivate', 'Inactivate'),
    ]
    status = models.CharField(max_length=10, choices=DISABLE_CHOICES, default='Activate')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    finish = models.ForeignKey(Finish,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.product.product_name +"-"+self.finish.title
    
    
class Location(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    godown_number = models.CharField(max_length=30)
    room_number=models.CharField(max_length=30)
    rack_number=models.CharField(max_length=30)

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=50)

@receiver(pre_save, sender=Product)
def update_main_category(sender, instance, **kwargs):
    if instance.sub_category:
        instance.main_category = instance.sub_category.main_category