from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
# Create your models here.

#Common Fields for every table

class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False,null=False)

    class Meta:
        abstract = True


# User Model 


class User(AbstractUser):

    username = None    # This is none because we will be defining the username later in the model.
    # password = models.CharField(max_length=30,default=None)
    phone_number = models.IntegerField(null=True,blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=250)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS =[]

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
    # item_image
    class Meta:
        db_table = 'Items'
    
    def __str__(self):
        return self.item_name
# Cart model 

class Cart(Common):
    user = models.ForeignKey(User, blank=False, null=False,on_delete=models.CASCADE)
    items = models.ManyToManyField(Items)

    class Meta:
        db_table = 'Cart'

    def __str__(self):
        return f"{self.user.email.trim('@gmail.com')} ({self.items.count()} items)" 
# Order Model

class Order(Common):
    MY_CHOICES = (
        ('Cash On Delivery', 'CASH ON DELIVERY'),
        ('upi', 'UPI'),
        ('card', 'CARD'),
    )
    cart = models.ForeignKey(Cart, blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    total_price = models.IntegerField(null=False, blank=False)
    payment_type = models.CharField('Payment Type',max_length=30,choices=MY_CHOICES)

    class Meta:
        db_table = 'Order'


    def __str__(self):
        return f"{self.user.email}'s Order)" 