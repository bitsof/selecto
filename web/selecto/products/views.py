from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Product, Review
from random import randint
import openai
from key import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Create your views here.

def home(request):
    product_list = Product.objects.all()
    if len(product_list) > 0 :
        p = product_list[ randint(0, len(product_list) - 1) ]
    else : 
        p = None
    if p == None:
        review_list = []
        r = None
    else:
        review_list = Review.objects.filter(review_related_product = p)
        if len(review_list) > 0 :
            r = review_list[ randint(0, len(review_list) - 1) ]
        else:
            r = None
    template = loader.get_template('products/home.html')
    context = {
        'product' : p,
        'review' : r,
        'product_list' : product_list,
        'review_list' : review_list,
    }
    return render(request, 'products/home.html', context)

def index(request):
    product_list = Product.objects.all()
    template = loader.get_template('products/index.html')
    test_string = "TEsting string"
    context = {
        'product_list': product_list,
        'test' : test_string,
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
    summary = ''
    definition = ''
    if(request.GET.get('define')):
        response = openai.Completion.create(
            model="text-curie-001",
            prompt="Define: " + str(request.GET.get('mytextbox')),
            temperature=0.6
        )
        definition = response.choices[0].text
        print(response)
        print(response.choices)
    if(request.GET.get('summarize')):
       response = openai.Completion.create(
            model="text-curie-001",
            max_tokens=1024,
            prompt="Summarize: " + str(review.review_content),
            temperature=0.6
        )
       print("Response : ", response.choices[0].text)
       print(response)
       print(response.choices)
       summary = response.choices[0].text
    context = {
        'review' : review,
        'definition' : definition,
        'summary' : summary,
    }
    return render(request, 'products/review_details.html', context)


