from django.db import models
from seller.models import *

# Create your models here.

#models are basically python classes and objects that represents datatbse table

class Buyer(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=150)
    address = models.TextField()
    pic = models.FileField(upload_to='profile_pics', default='prof.jpg')

    def __str__(self):
        return self.email


class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)