from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Finish(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class MainCategory(models.Model):
    image = models.ImageField(upload_to='category', null=True, blank=True)
    category_name = models.CharField(max_length=255)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='subcategory', null=True, blank=True)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.sub_category_name

class Role(models.Model):
    title = models.CharField(_("Title"), max_length=10)
    def __str__(self):
        return self.title

class SizeChart(models.Model):
    disable = models.BooleanField(default=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True)
    finish = models.ForeignKey(Finish,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"{self.product.product_name} - {self.size}"

class RolePrice(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeChart, on_delete=models.CASCADE,null=True,blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    price_with_gst = models.DecimalField(max_digits=20,decimal_places=2,null=True)

    def __str__(self):
        return f"{self.role.title} - {self.price}"

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product', null=True, blank=True)
    stock_quantity = models.IntegerField()
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    sku_code = models.CharField(max_length=30,null=True,blank=True)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

class MultiImages(models.Model):
    image = models.ImageField(upload_to="product_multi_images")
    prod_img = models.ForeignKey("ProductImage", verbose_name=_("Product Image"), on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.image.name

class ProductImage(models.Model):
    disable = models.BooleanField(default=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    finish = models.ForeignKey(Finish,on_delete=models.CASCADE,null=True)
    # image = models.ManyToManyField(MultiImages)
    
class Location(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    godown_number = models.CharField(max_length=30)
    room_number=models.CharField(max_length=30)
    rack_number=models.CharField(max_length=30)

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=50)