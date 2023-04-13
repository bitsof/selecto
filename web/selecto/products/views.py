from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Product, Review

# Create your views here.

def index(request):
    product_list = Product.objects.all()
    template = loader.get_template('products/index.html')
    context = {
        'product_list': product_list,
    }
    return render(request, 'products/index.html', context)

def details(request, product_id):
    product = Product.objects.get(id=product_id)
    review_list = Review.objects.filter(review_related_product = product)
    template = loader.get_template('products/details.html')
    context = {
        'product': product, 'review_list' : review_list,
    }
    return render(request,'products/details.html', context )

def review_details(request, product_id, review_id):
    review = Review.objects.get(id = review_id)
    template = loader.get_template('products/review_details.html')
    context = {
        'review' : review,
    }
    return render(request, 'products/review_details.html', context)

def test(request):
    return HttpResponse('test')


