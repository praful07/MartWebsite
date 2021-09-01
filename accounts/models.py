from django.db import models
import datetime

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    order_date = models.DateField(auto_now_add=True,null=True)

class Join(models.Model):
    customer_id = models.IntegerField()
    order_id = models.IntegerField()
