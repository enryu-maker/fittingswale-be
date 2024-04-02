from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
import uuid

class Finish(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class MainCategory(models.Model):
    image = models.ImageField(upload_to='main_category', null=True, blank=True)
    main_category_name = models.CharField(max_length=50,null=True)
    DISABLE_CHOICES = [
        ('Activate', 'Activate'),
        ('Inactivate', 'Inactivate'),
    ]
    status = models.CharField(max_length=10, choices=DISABLE_CHOICES, default='Activate')
    
    def __str__(self):
        return self.main_category_name

class Category(models.Model):
    main_category = models.ForeignKey(MainCategory,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='category',null=True,blank=True)
    category_name = models.CharField(max_length=50,null=True)
    DISABLE_CHOICES = [
        ('Activate', 'Activate'),
        ('Inactivate', 'Inactivate'),
    ]
    status = models.CharField(max_length=10, choices=DISABLE_CHOICES, default='Activate')
    
    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    sub_category_name = models.CharField(max_length=50)
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
    sku_code = models.CharField(max_length=30,null=True,blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=255,null=True)
    # quantity = models.IntegerField(null=True)
    minimum_stock_quantity = models.PositiveIntegerField(null=True)
    finish = models.ForeignKey(Finish,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"{self.product.product_name} - {self.size}"

class RolePrice(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeChart, on_delete=models.CASCADE,null=True,blank=True)
    gst_percent = models.DecimalField(max_digits=20, decimal_places=2,default=18,null=True)
    price_with_gst = models.DecimalField(max_digits=20,decimal_places=2,null=True)
    minimum_order_quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.role.title} - {self.price_with_gst}"

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='product', null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE,null=True)
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
    # product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    godown_number = models.CharField(max_length=30)
    room_number=models.CharField(max_length=30)
    rack_number=models.CharField(max_length=30)
    size = models.ForeignKey(SizeChart,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.size.size+" - Location"
    

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=50)
    
    def __str__(self):
        return self.product.product_name+" - "+self.name
    
class PaymentTransaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('online', 'Online'),
        ('bank_transfer', 'Bank Transfer'), 
        ('cod', 'COD'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # currency = models.CharField(max_length=3)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True)
    items = models.JSONField()
    address = models.JSONField()
    contact_details = models.JSONField(null=True)
    # muid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total = models.DecimalField(decimal_places=2,max_digits=20)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())[:8]  # Generate a random 8-character string as transaction ID
        super().save(*args, **kwargs)

class Stock(models.Model):
    size_chart = models.OneToOneField(SizeChart, on_delete=models.CASCADE, related_name='stock_quantity')
    stock_quantity = models.IntegerField(validators=[MinValueValidator(0)],null=True)
    

@receiver(pre_save, sender=Product)
def update_main_category(sender, instance, **kwargs):
    if instance.sub_category:
        instance.category = instance.sub_category.category
        print(instance.category)
        instance.main_category = instance.category.main_category