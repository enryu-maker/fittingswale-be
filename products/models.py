from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class MainCategory(models.Model):
    image = models.ImageField(upload_to='category', null=True, blank=True)
    category_name = models.CharField(max_length=255)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=255)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.sub_category_name


class Role(models.Model):
    title = models.CharField(_("Title"), max_length=10)
    def __str__(self):
        return self.title


class RolePrice(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.role.title} - {self.product.product_name} - {self.price}"


class SizeChart(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.product.product_name} - {self.size}"


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product', null=True, blank=True)
    stock_quantity = models.IntegerField()
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name


class Finish(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    finish = models.ForeignKey(Finish,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to="product_images", height_field=None, width_field=None, max_length=None)
