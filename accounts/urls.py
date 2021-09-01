from django.contrib import admin
from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('addproduct/',views.createProduct,name='addproduct'),
    path('updateproducts/<str:pk>/',views.updateProduct,name='updateproducts'),
    path('deleteproduct/<str:pk>',views.deleteProduct,name='deleteproducts'),

    path('customers/',views.customers,name='customers'),
    path('cutomer_profile/<str:pk>',views.customerprofile,name='customerprofile'),
    path('update_cutomer_profile/<str:pk>',views.updateCustomer,name='updatecustomerprofile'),
    path('add_customer',views.addcustomer,name='addcustomer'),

    path('order/<str:pk>',views.order,name='order'),
    path('add_order/<str:cus_id>',views.add_order,name='add_order'),
    path('save_order/<str:cus_id>',views.save_order,name='save_order'),
    path('update_order/<str:order_id>/<int:cus_id>/',views.update_order,name='update_order'),
    path('delete_order/<str:order_id>/<int:cus_id>/',views.delete_order,name='delete_order'),
    path('orders_by_date/<str:day>/<str:month>/<str:year>/<str:cus_id>',views.orders_by_date,name='orders_by_date'),
    path('invoice/<str:day>/<str:month>/<str:year>/<str:cus_id>',views.get_invoice,name='invoice'),
]