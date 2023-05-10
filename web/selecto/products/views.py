from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Product, Review
from .forms import CustomUserCreationForm
from random import randint
from config import GOOGLE_CLIENT_ID
from . import openai_module
from products.serializers import ProductSerializer, ReviewSerializer, UserSerializer
from rest_framework import generics, renderers, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from dataaccesslayer import get_all_products

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
        'page_title' : 'Selecto',
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
        'page_title' : 'Selecto - Index',
        'product_list': product_list,
    }
    return render(request, 'products/index.html', context)

def details(request, product_id):
    product = Product.objects.get(id=product_id)
    review_list = Review.objects.filter(review_related_product = product)
    template = loader.get_template('products/details.html')
    page_title = 'Selecto - ' + product.product_name
    context = {
        'page_title' : page_title,
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
        'page_title' : 'Selecto - Review',
        'review' : review,
        'definition' : definition,
        'summary' : summary,
    }
    return render(request, 'products/review_details.html', context)

def contact_us(request):
    templete = loader.get_template('products/contact_us.html')
    context = {
        'page_title' : 'Selecto - Contact Us'
    }
    return render(request, 'products/contact_us.html', context)

def about_us(request):
    template = loader.get_template('products/about_us.html')
    context = {
        'page_title' : 'Selecto - About Us'
    }
    return render(request, 'products/about_us.html', context)

def logout_view(request):
    logout(request)
    return redirect("/")

def login(request):
    context = {
        'page_title' : 'Selecto - Log In',
        'google_client_id':GOOGLE_CLIENT_ID,
        'host_name':'http://localhost:8000/login/'
    }
    template = loader.get_template('products/login.html')
    return render(request, 'products/login.html', context)

def signup(request):
    template = loader.get_template('products/signup.html')
    context = {
        'page_title' : 'Selecto - Sign Up',
    }
    return render(request, 'products/signup.html', context)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'products/signup.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({
                'success': False,
                'errors': form.errors.as_text(),
            }, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return JsonResponse({
                'success': True,
                'redirect': self.success_url,
            })
        else:
            return response
        
'''
These are generic class based views. Implements a lot so it saves on boilerplate code.
https://www.django-rest-framework.org/tutorial/3-class-based-views/
'''
'''
The classes that inherit from ListCreateAPIView handles GET and POST requests, 
while classes that inherit from RetrieveUpdateDestroyAPIView handles GET, 
PUT, PATCH, and DELETE requests.
'''
class ApiProductList(generics.ListCreateAPIView):
    queryset = get_all_products()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ApiProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_all_products()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ApiReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ApiReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserList(generics.ListAPIView):
    # While the other classes had models whose ordering was defined through
    # the meta class, instead users is ordered by username here.
    queryset = User.objects.order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetail(generics.RetrieveAPIView):
    # While the other classes had models whose ordering was defined through
    # the meta class, instead users is ordered by username here.
    queryset = User.objects.order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

'''
The api_root function is a simple view that returns a dictionary of available API endpoints, 
represented as URLs. It uses the DRF reverse function to generate the URLs dynamically, 
based on the URL patterns defined in the project's urls.py file.
'''
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # gets the url from urls.py
        'users': reverse('products:api_user_list', request=request, format=format),
        'products': reverse('products:api_product_list', request=request, format=format),
        'reviews': reverse('products:api_review_list', request=request, format=format),
    })
