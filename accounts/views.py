from typing import BinaryIO
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filter import *
from datetime import date
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse, response
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
# Create your views here.


def home(request):
    orders = Order.objects.filter(order_date=date.today())
    join = Join.objects.all()
    products = []
    dic_prod = {}
    order_count = 0
    order_id = []
    sales = 0
    l = set()
    for i in orders:
        sales = sales + (i.product.price*i.quantity)
        order_id.append(i.id)
        products.append(i.product.name)

    total_products = set(products)
    
    for i in total_products:
        dic_prod[i] = products.count(i)
    
    for i in join:
        if i.customer_id not in l and i.order_id in order_id:
            order_count += 1
            l.add(i.customer_id)
            
    context = {'order_count':order_count,'sales':sales,'dic_prod':dic_prod}
    return render(request, 'accounts/dashboard.html', context)

def customerprofile(request, pk):
    customer = Customer.objects.get(id=pk)
    order_ids = Join.objects.filter(customer_id=pk)
    dates = []
    for i in order_ids:
        x = [Order.objects.get(id=i.order_id).order_date.day,Order.objects.get(id=i.order_id).order_date.month,Order.objects.get(id=i.order_id).order_date.year]
        if x not in dates:
            dates.append(x)
    dates.reverse()
    context = {'customer': customer,'dates':dates}
    return render(request, 'accounts/customer_profile.html', context)

def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    context = {'form': form,'cus_id':pk}
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            redirect_url = reverse('customerprofile',args=[pk])
            return HttpResponseRedirect(redirect_url)
    return render(request, 'accounts/update_customer_profile.html', context)

def addcustomer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {'form': form}
    return render(request, 'accounts/add_customer.html', context)

def customers(request):
    customers = Customer.objects.all()
    myFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myFilter.qs
    context = {'customers': customers, 'myFilter': myFilter}

    return render(request, 'accounts/customers.html', context)


def products(request):
    product = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=product)
    product = myFilter.qs

    context = {'products': product, 'myFilter': myFilter}
    return render(request, 'accounts/products.html', context)


def createProduct(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, 'accounts/add_product.html', context)


def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, 'accounts/update_products.html', context)


def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == "POST":
        product.delete()
        return redirect('products')

    context = {'form': form}
    return render(request, 'accounts/delete_product.html', context)


def order(request, pk):
    cus_id = pk
    order_id_objs = Join.objects.filter(customer_id=cus_id)
    lst = []
    total_price = 0
    for i in order_id_objs:
        num = int(i.order_id)
        if Order.objects.filter(id=num,order_date=date.today()).exists():
            lst.append([Order.objects.get(id=num),Order.objects.get(id=num).product.price*Order.objects.get(id=num).quantity])
            total_price += Order.objects.get(id=num).product.price*Order.objects.get(id=num).quantity
        lst = (list(lst))
    context = {'cus_id': pk, 'order': lst,'price':total_price,'day':date.today().day,'month':date.today().month,'year':date.today().year}
    return render(request, 'accounts/order.html', context)


def add_order(request, cus_id):
    form = OrderForm()
    context = {'form': form, 'cus_id': cus_id}
    return render(request, 'accounts/add_order.html', context)


def save_order(request, cus_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
    odr_id = Order.objects.last()

    obj = Join(customer_id=cus_id, order_id=odr_id.id)
    obj.save()

    order_id_objs = Join.objects.filter(customer_id=cus_id)
    lst = []
    total_price = 0
    for i in order_id_objs:
        num = int(i.order_id)
        if Order.objects.filter(id=num,order_date=date.today()).exists():
            lst.append([Order.objects.get(id=num),Order.objects.get(id=num).product.price*Order.objects.get(id=num).quantity])
            total_price += Order.objects.get(id=num).product.price*Order.objects.get(id=num).quantity
        lst = (list(lst))
    
    context = {'cus_id': cus_id, 'order': lst,'price':total_price,'day':date.today().day,'month':date.today().month,'year':date.today().year}
    return render(request, 'accounts/order.html', context)


def update_order(request, order_id,cus_id):
    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            #return redirect('customers')
            order_id_objs = Join.objects.filter(customer_id=cus_id)
            lst = []
            total_price = 0
            for i in order_id_objs:
             num = int(i.order_id)
             if Order.objects.filter(id=num,order_date=date.today()).exists():
              lst.append([Order.objects.get(id=num),Order.objects.get(id=num).product.price*Order.objects.get(id=num).quantity])
              total_price += Order.objects.get(id=num).product.price*Order.objects.get(id=num).quantity
              lst = (list(lst))
              redirect_url = reverse('order',args=[cus_id])
              return HttpResponseRedirect(redirect_url)
    context = {'form': form,'cus_id':cus_id}
    return render(request, 'accounts/update_order.html', context)

def delete_order(request, order_id,cus_id):
    order = Order.objects.get(id=order_id)
    join = Join.objects.get(order_id=order_id)
    form = OrderForm(instance=order)
    if request.method == "POST":
        order.delete()
        join.delete()
        order_id_objs = Join.objects.filter(customer_id=cus_id)
        lst = []
        total_price = 0
        for i in order_id_objs:
            num = int(i.order_id)
            if Order.objects.filter(id=num,order_date=date.today()).exists():
              lst.append([Order.objects.get(id=num),Order.objects.get(id=num).product.price*Order.objects.get(id=num).quantity])
              total_price += Order.objects.get(id=num).product.price*Order.objects.get(id=num).quantity
              lst = (list(lst))
            redirect_url = reverse('order',args=[cus_id])
            return HttpResponseRedirect(redirect_url)
    context = {'form': form,'cus_id':cus_id}
    return render(request, 'accounts/delete_order.html', context)

def orders_by_date(request,day,month,year,cus_id):
    order_id_objs = Join.objects.filter(customer_id=cus_id)
    lst = []
    total_price = 0
    for i in order_id_objs:
        x = Order.objects.get(id=i.order_id).order_date
        if x.day == int(day) and x.month == int(month) and x.year == int(year):
            lst.append([Order.objects.get(id=i.order_id),Order.objects.get(id=i.order_id).product.price*Order.objects.get(id=i.order_id).quantity])
            total_price += Order.objects.get(id=i.order_id).product.price*Order.objects.get(id=i.order_id).quantity
        lst = (list(lst))
    date = [day,month,year]
    print(lst,day,month,year,Order.objects.get(id=i.order_id).order_date.day)
    context = {'cus_id': cus_id, 'order': lst,'price':total_price,'day':day,'month':month,'year':year}
    return render(request,'accounts/orders_by_date.html',context)

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    return HttpResponse(result.getvalue(),content_type='applcation.pdf')

def get_invoice(request,day,month,year,cus_id):
    order_id_objs = Join.objects.filter(customer_id=cus_id)
    customer = Customer.objects.get(id=cus_id)
    lst = []
    total_price = 0
    for i in order_id_objs:
        x = Order.objects.get(id=i.order_id).order_date
        if x.day == int(day) and x.month == int(month) and x.year == int(year):
            lst.append([Order.objects.get(id=i.order_id),Order.objects.get(id=i.order_id).product.price*Order.objects.get(id=i.order_id).quantity])
            total_price += Order.objects.get(id=i.order_id).product.price*Order.objects.get(id=i.order_id).quantity
        lst = (list(lst))
    
    context = {'customer': customer, 'order': lst,'price':total_price,'day':day,'month':month,'year':year}
    pdf = render_to_pdf('accounts\invoice.html',context)
    if pdf:
        response = HttpResponse(pdf,content_type='application.pdf')
        filename = "Invoice_%s.pdf" %(cus_id)
        content = "inline; filename='%s'" %(filename)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not Found")




