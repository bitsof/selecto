from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
from .models import Product, Review, ProductPhoto
from random import randint
from config import GOOGLE_CLIENT_ID
from . import openai_module
from products.serializers import ProductSerializer, ReviewSerializer, UserSerializer
from rest_framework import generics, renderers, permissions
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from dataaccesslayer import get_all_products
from .utils import get_page_title
from django.contrib.auth.decorators import login_required

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
        'page_title' : get_page_title('home'),
        'product' : p,
        'review' : r,
        'product_list' : product_list,
        'review_list' : review_list,
    }
    return render(request, 'products/home.html', context)

def login(request):
    context = {
        'page_title' : get_page_title('login'),
        'google_client_id':GOOGLE_CLIENT_ID,
        'host_name':'http://localhost:8000/login/'
    }
    template = loader.get_template('products/login.html')
    return render(request, 'products/login.html', context)

class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['page_title'] = get_page_title('index')
        return context

class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_list'] = Review.objects.filter(review_related_product=self.get_object().id)
        context['page_title'] = get_page_title('details', self.get_object().product_name)
        context['photo_list'] = ProductPhoto.objects.filter(photo_related_product=self.get_object().id)
        return context

class ReviewDetailView(generic.DetailView):
    model = Review
    content_object_name = 'review'
    template_name = 'products/review_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = get_page_title('review_details', Product.objects.get(id=self.get_object().review_related_product.id).product_name)
        
        return context
    
def contact_us(request):
    templete = loader.get_template('products/contact_us.html')
    context = {
        'page_title' : get_page_title('contact_us')
    }
    return render(request, 'products/contact_us.html', context)

def about_us(request):
    template = loader.get_template('products/about_us.html')
    context = {
        'page_title' : get_page_title('about_us')
    }
    return render(request, 'products/about_us.html', context)

def logout_view(request):
    logout(request)
    return redirect("/")

def signup(request):
    template = loader.get_template('products/signup.html')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect to success page
            return redirect('products/home.html')
    else:
        form = SignUpForm()
    context = {
        'page_title' : get_page_title('signup'),
        'form': form
    }
    return render(request, 'products/signup.html', context)


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
    permission_classes = [IsAdminOrReadOnly]

class ApiProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_all_products()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ApiReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly]

class ApiReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly]

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
