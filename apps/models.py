from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from cloudinary.models import CloudinaryField
import secrets
# Create your models here.

#Common Fields for every table

class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False,null=False)

    class Meta:
        abstract = True


# User Model 


class User(AbstractUser):
    username = models.CharField(max_length=250,null=True,blank=True,unique=True)
    password = models.CharField(max_length=100,default=None,null=True,blank=True)
    phone_number = models.IntegerField(null=True,blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=250)
    jwt_token = models.CharField(max_length=250,unique=True,null=True)
    token = models.CharField(max_length=100,unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    display_picture = CloudinaryField('Display Picture',null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS =['username','phone_number']

    
    # function to create a token 
    def save_token(self, *args, **kwargs):
        if not self.token:
            # generate new token if none exists
            self.token = secrets.token_urlsafe(32)

        super().save(*args, **kwargs)

    
    def update_token(self):
        self.token = None
        self.token_created = None
        self.token_expires = None
        self.save()

    # def get_token_expiry(self):
    #     if self.token_expiry:
    #         return timezone.localtime(self.token_expiry)
    #     else:
    #         return None
# Category Model

class Categories(Common):
    category_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Categories'

    def __str__(self):
        return self.category_name
    
# Items Model

class Items(Common):
    
    category = models.ForeignKey(Categories,on_delete=models.SET_DEFAULT,default='all')
    item_name = models.CharField('Item Name',max_length=50,blank=False,null=False)
    item_price = models.FloatField('Item Price',null=False,blank=False)
    item_image = CloudinaryField('Item Image',null=False,blank=False)
    is_available = models.BooleanField('Is Available',default=True)
    
    class Meta:
        db_table = 'Items'
    
    def __str__(self):
        return self.item_name

class Cart(models.Model):
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=False,on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=False, default=1)
    
    class Meta:
        db_table = 'Cart'
    
    

# Order Model

class Order(Common):
    MY_CHOICES = (
        ('Cash On Delivery', 'CASH ON DELIVERY'),
        ('upi', 'UPI'),
        ('card', 'CARD'),
    )
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    address = models.CharField(max_length=100,null=False,blank=False)
    zip_code = models.IntegerField(null=False, blank=False)
    place = models.CharField(max_length=100,null=False,blank=False)
    payment_method = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table = 'Order'


    def __str__(self):
        return f"{self.user.username}'s Order)" 
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete= models.CASCADE)
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    total_price = models.IntegerField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)