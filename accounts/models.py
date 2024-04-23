from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, UserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
import string
from products.models import Product
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Change the default User Model beahavier to login with 'email'.
    """
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=30, blank=True)
    mobile_no = models.CharField(_('MobNumber'), null=True, blank=True,unique=True)
    pan_no = models.CharField(_('PanNumber'), max_length=50,null=True, blank=True,unique=True)
    gst_no = models.CharField(_('GstNumber'),  max_length=50,null=True, blank=True,unique=True)
    pan_card = models.FileField(upload_to="pancards", max_length=254,null=True,blank=True)
    gst_certificate = models.FileField(upload_to="gstcertificates", max_length=254,null=True,blank=True)
    role = models.CharField(_('Role'), max_length=70, null=True, blank=True)
    otp = models.IntegerField(null=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_(
        'Designates whether the user can log into this admin site')
    )
    
    is_verify = models.BooleanField(_('Verified'), default=False, help_text=_(
        'Designates whether this user has Verified his account.')
    )
    
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting account')
    )
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    
    
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_(
        'Designates whether this user has confirmed his account.')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return self.name
    
    def is_profile_complete(self):
        """
        Method to check if the user's profile is complete.
        """
        if self.pan_no is not None and self.gst_no is not None and self.pan_card and self.gst_certificate:
            return True
        return False
    
    def save(self, *args, **kwargs):
        if not self.is_verify and self.is_profile_complete() and not self.role=="Customer":
            subject = 'Profile KYC Request'
            message = f'To Verify This Profile Please visit :https://api-nerdtech.fittingswale.in/admin/accounts/user/{self.id}/change/'
            from_email = 'itsriteshmahale2002@gmail.com'
            to_email = ['rahulmittal7878@gmail.com','riteshmahale15@gmail.com',"akifkhan60067@gmail.com"]
            send_mail(subject, message, from_email, to_email)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'user'

class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name if self.user.name else "Unknown User"

class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_settings = models.BooleanField(default=True)
    privacy_settings = models.BooleanField(default=True)
    # add other user-specific settings
    def __str__(self):
        return self.user.name
    
class Coupons(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=50)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
    
    def __str__(self):
        return self.user.name

class RatingAndReviews(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    # add other review-related fields
    def __str__(self):
        return self.user.name

class StarCoins(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    star_coins_balance = models.IntegerField(default=0)

class OrderHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name
    
