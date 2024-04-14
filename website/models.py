from products.models import Product
from django.db import models

class BestSellerProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='bestseller_product')

    def __str__(self):
        return self.product.product_name + " - Bestseller"

class SpotlightProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='spotlight_product')

    def __str__(self):
        return self.product.product_name + " - Spotlight"