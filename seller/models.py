from django.db import models

# Create your models here.

class Seller(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    pic = models.FileField(upload_to='seller_pics', default='prof.jpg')
    password = models.CharField(max_length=150)
    gst_no = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=150)
    des = models.TextField()
    price = models.FloatField()
    pic = models.FileField(upload_to='product_pics', default='prof.jpg')
    seller = models.ForeignKey(Seller, on_delete= models.CASCADE)

    # def __str__(self) -> str:
    #     return self.name

class SellerOrderHistory(models.Model):
    s1 = [('order placed', 'order placed'),
          ('out for delivery', 'out for delivery')]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(to='Buyer.Buyer', on_delete=models.CASCADE)
    status = models.CharField(max_length=150, choices=s1, default='order placed')