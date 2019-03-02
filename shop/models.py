from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
# Create your models here.
class AddressOne(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.PositiveIntegerField()
    pincode = models.PositiveIntegerField()
    locality = models.TextField()
    address = models.TextField() 
    choices = (
        ('CITY','City'),
        ('DISTRICT','District'),
        ('TOWN','Town'),
    )
    city_district_town =  models.CharField(max_length=50,choices=choices,default='CITY')
    state = models.CharField(max_length=20)
    landmark = models.CharField(max_length=50)
    type_choices = (
        ('HOME','Home'),
        ('WORK','Work'),
    )
    address_type = models.CharField(max_length = 50,choices =type_choices,default='HOME')
class AddressTwo(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.PositiveIntegerField()
    pincode = models.PositiveIntegerField()
    locality = models.TextField()
    address = models.TextField() 
    choices = (
        ('CITY','City'),
        ('DISTRICT','District'),
        ('TOWN','Town'),
    )
    city_district_town =  models.CharField(max_length=50,choices=choices,default='CITY')
    state = models.CharField(max_length=20)
    landmark = models.CharField(max_length=50)
    type_choices = (
        ('HOME','Home'),
        ('WORK','Work'),
    )
    address_type = models.CharField(max_length = 50,choices =type_choices,default='HOME')


    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.name 

class Bucket(models.Model):
    name = models.CharField(max_length=100,null=True)
    files = models.ForeignKey(File,on_delete=models.CASCADE)

class CustomUser(AbstractUser):
    choices = (
        ('SELLER','Seller'),
        ('BUYER','Buyer'),
        ('ADMIN','Admin'),
        ('DEVICE_MANUFACTURER','Device_Manufacturer'),
    )
    usertype = models.CharField(max_length=50,choices=choices,default='BUYER')
    user_slug = models.SlugField(max_length=25,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    address_one = models.OneToOneField(AddressOne,on_delete=models.SET_NULL,null=True)
    address_two = models.OneToOneField(AddressTwo,on_delete=models.SET_NULL,null=True)
     
    def get_absolute_url(self):
        return reverse('view_user', kwargs={'username': self.username})

    def __str__(self):
        return self.username

class Specification(models.Model):
    version = models.CharField(max_length=10)
    hw_specification = models.TextField()
    sw_specification = models.TextField()
    support_notes = models.TextField()

    class Meta:
        ordering=('id',)


class Component(models.Model):
    name = models.CharField(max_length=50)
    specification =  models.ForeignKey(Specification,on_delete=models.SET_NULL,null=True)
    added = models.DateTimeField(auto_now_add=True)
    model_number = models.CharField(max_length=30)
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.username)

class Device(models.Model):
    name = models.CharField(max_length=50)
    specification =  models.ForeignKey(Specification,on_delete=models.SET_NULL,null=True)
    components = models.ManyToManyField(Component,related_name='components')
    manufacturer = models.ForeignKey(CustomUser,related_name='device_manufacturer',on_delete=models.SET_NULL,null=True)
    sellers = models.ManyToManyField(CustomUser,related_name='sellers')
    model_number = models.PositiveIntegerField()
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.name)
class Banner(models.Model):
    seller = models.ForeignKey(CustomUser,related_name='banner_seller',on_delete=models.CASCADE)
    device = models.ForeignKey(Device,related_name='banner_device',on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return "{} {}".format(str(self.seller),str(self.device))

class Cart(models.Model):
    buyer = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='buyer_cart')
    updated = models.DateTimeField(auto_now=True)
    banners = models.ManyToManyField(Banner,related_name='banner_cart')

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.buyer.username)


class Payment(models.Model):
    payment_choices = (
        ('COD','COD'),
        ('DEBIT CARD','Debit Card'),
        ('CREDIT CARD','Credit Card'),
        )
    amount = models.PositiveIntegerField()

class Order(models.Model):
    buyer = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name='buyer_order')
    banners= models.ManyToManyField(Banner,related_name='banner_order')
    date = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)
    status_choices = (
        ('SHIPPED','Shipped'),
        ('DISPATCHED','Dispatched'),
        ('APPROVED','Approved'),
        ('DELIVERED','Delivered'),
    )
    status = models.CharField(max_length=50,choices=status_choices,null=True)
    delivery_data = models.DateTimeField(null=True)

    amount = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.buyer.username)


class Wishlist(models.Model):
    buyer = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='buyer_wishlist')
    updated = models.DateTimeField(auto_now=True)
    banners = models.ManyToManyField(Banner,related_name='banner_wishlist')

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.buyer.username)



    
