import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
  class Meta:
      model = Product
      
      fields = {
          'name': ['icontains'],
          'price': ['icontains'],
          'category': ['icontains'],
      }


class CustomerFilter(django_filters.FilterSet):
  class Meta:
    model = Customer
    fields = {
      'name':['icontains'],
      'email':['icontains'],
      'phone':['icontains'],
    }

class OrderFilter(django_filters.FilterSet):
  class Meta:
    model = Order
    fields = {
      'order_date':['icontains']
    }