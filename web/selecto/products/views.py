from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Product, Review
from .forms import SignUpForm
from random import randint
from config import GOOGLE_CLIENT_ID
from . import openai_module

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
    summary = ''
    definition = ''
    if(request.GET.get('define')):
        response, definition = openai_module.define(request.GET.get('mytextbox'))
        print(response)
        print(response.choices)
    if(request.GET.get('summarize')):
       response, summary = openai_module.summarize(review.review_content)
       print("Response : ", response.choices[0].text)
       print(response)
       print(response.choices)
    context = {
        'review' : review,
        'definition' : definition,
        'summary' : summary,
    }
    return render(request, 'products/review_details.html', context)

def contact_us(request):
    templete = loader.get_template('products/contact_us.html')
    return render(request, 'products/contact_us.html', {})

def about_us(request):
    template = loader.get_template('products/about_us.html')

    return render(request, 'products/about_us.html')

def logout_view(request):
    logout(request)
    return redirect("/")

def login(request):
    context = {
        'google_client_id':GOOGLE_CLIENT_ID,
        'host_name':'http://localhost:8000/login/'
    }
    template = loader.get_template('products/login.html')
    return render(request, 'products/login.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # additional validation for username and email
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
                return render(request, 'signup.html', {'form': form})
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists')
                return render(request, 'signup.html', {'form': form})
            # set user password and save
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            # authenticate and login user
            user = authenticate(username=username, password=password)
            login(request, user)
            # redirect to success page
            return redirect('success')
    else:
        form = SignUpForm()
    return render(request, 'products/signup.html', {'form': form})
