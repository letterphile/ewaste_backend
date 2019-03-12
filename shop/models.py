from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
# Create your models here.
class AddressOne(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
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
    phone_number = models.CharField(max_length=10)
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

class CustomUser(AbstractUser):
    choices = (
        ('SELLER','Seller'),
        ('BUYER','Buyer'),
        ('ADMIN','Admin'),
    )
    usertype = models.CharField(max_length=50,choices=choices,default='BUYER')
    user_slug = models.SlugField(max_length=25,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    address_one = models.OneToOneField(AddressOne,on_delete=models.SET_NULL,null=True)
    address_two = models.OneToOneField(AddressTwo,on_delete=models.SET_NULL,null=True)
    phone_number = models.CharField(max_length=10,null=True)    
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
    manufacturer = models.ForeignKey('Manufacturer',on_delete = models.CASCADE)
    sellers = models.ManyToManyField(CustomUser)
    description = models.TextField(null=True)
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.username)

class Device(models.Model):
    name = models.CharField(max_length=50)
    specification =  models.ForeignKey(Specification,on_delete=models.SET_NULL,null=True)
    components = models.ManyToManyField(Component,related_name='components')
    reuse_method = models.TextField(blank=True) 
    manufacturer = models.ForeignKey('Manufacturer',on_delete = models.CASCADE)
    sellers = models.ManyToManyField(CustomUser)
    model_number = models.CharField(max_length=50)
    added = models.DateTimeField(auto_now_add=True)
    price = models.CharField(max_length=10,null=True)
    description = models.TextField(null=True)

    file = models.ForeignKey(File,on_delete=models.SET_NULL,null=True) 
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

class CartToDevice(models.Model):
    cart = models.ForeignKey('Cart',on_delete=models.CASCADE)
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
class CartToComponent(models.Model):
    cart = models.ForeignKey('Cart',on_delete=models.CASCADE)
    component= models.ForeignKey(Component,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Cart(models.Model):
    buyer = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='buyer_cart')
    updated = models.DateTimeField(auto_now=True)
    components = models.ManyToManyField(Component)
    devices = models.ManyToManyField(Device) 
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
    devices = models.ManyToManyField(Device)
    components= models.ManyToManyField(Component)
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.buyer.username)



    
class Manufacturer(models.Model):
    name= models.CharField(max_length=50)
    description=models.TextField()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.name)