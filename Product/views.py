from django.shortcuts import render
import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from .forms import *

from .models import Product

# Create your views here.
def Product_Page(request):
    if request.method=='POST':
        form = Product_Forms(request.POST)
        if form.is_valid():
            form.save()
        form = Product_Forms()
        product = Product.objects.all()
        return render(request, 'Product/index.html', {'product': product, 'form':form})
        
    form = Product_Forms()
    product = Product.objects.all()
    return render(request, 'Product/index.html', {'product': product, 'form':form})

def Update_Product(request, pk):
    if request.method=='POST':
        product = Product.objects.get(id=pk)
        form = Product_Forms(request.POST, instance=product)
        if form.is_valid():
            form.save()
        form = Product_Forms()
        product = Product.objects.all()
        return render(request, 'Product/index.html', {'product': product, 'form':form})
    product = Product.objects.get(id=pk)
    form = Product_Forms(instance=product)
    return render(request, 'Product/update.html', {'product': product, 'form':form})

def Delete_Product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    form = Product_Forms()
    product = Product.objects.all()
    return render(request, 'Product/index.html', {'product': product, 'form':form})  

def Category_Page(request):
    return render(request, 'Product/category.html')

def Search_Product(request):
    product_search = request.GET['product_name']
    product_search_obj = Product.objects.filter(name__icontains=product_search)
    return render(request, 'Product/search.html', {'product_search_obj':product_search_obj})
    # product_search = request.GET['product']
    # product_obj = Product.objects.filter(name__icontains=product_search)
    # post_list = serializers.serialize('json', product_obj)
    # return HttpResponse(post_list, content_type="text/json-comment-filtered")
    # return JsonResponse(product_obj, safe=True)

def Detail_Product(request, pk):
    product_obj = Product.objects.get(id = pk)
    return render(request, 'Product/detail_product.html',{'product':product_obj})

