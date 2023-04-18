import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selecto.settings')
import django
django.setup()
import sys

from django.utils import timezone
from products.models import Product, Review, ProductPhoto, Store, StoreLink 

# creates a product, saves it, and returns that same product
def make_product(name, description):
    p = Product(product_name = name, product_description = description)
    p.save()
    return p

# deletes a product
def delete_product(product):
    product.delete()
    return

# returns a list of all products
def get_all_products():
    return Product.objects.all()

# gets all products that matches name
# for example get_all_products('tripod') would return all products with tripod in the name or description
def get_all_products_by_name(name):
    return

def get_product_by_id(id):
    p = Product.objects.get(id = id)
    return p

def get_product_by_name(name):
    return

# also write functions to create, get, and delete review, productphoto, store, and store link
# for the review function make, if there is no time zone included make it to default to timezone.now()
# also write get functions for each of the types of models, for fields that make sense. You should
# write different functions for getting something for each field that makes sense, instead of overloading
# the function.

