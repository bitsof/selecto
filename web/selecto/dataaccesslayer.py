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

def delete_product_by_id(id):
    p = Product.objects.get(id = id)
    p.delete()
    return

# returns a list of all products
def get_all_products():
    return Product.objects.all()

# gets all products that matches name
def get_all_products_by_name(name):
    return Product.objects.filter(name = name)

def get_product_by_id(id):
    p = Product.objects.get(id = id)
    return p
