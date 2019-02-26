from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
# Create your models here.

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

    def get_absolute_url(self):
        return reverse('view_user', kwargs={'username': self.username})

    def __str__(self):
        return self.username

class Component(models.Model):
    name = models.CharField(max_length=50)
    specs = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    model_number = models.PositiveIntegerField()
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.name)


class Device(models.Model):
    name = models.CharField(max_length=50)
    components = models.ManyToManyField(Component,related_name='components')
    sellers = models.ManyToManyField(CustomUser,related_name='sellers')
    price = models.PositiveIntegerField()
    model_numer = models.PositiveIntegerField()
    added = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.name)

class Cart(models.Model):
    buyer = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='buyer_cart')
    items = models.ManyToManyField(Device,related_name='items_cart')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.buyer.name)

class Order(models.Model):
    buyer = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name='buyer_order')
    items = models.ManyToManyField(Device,related_name='items_order')
    date = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
    def __str__(self):
        return str(self.buyer.name)




    
