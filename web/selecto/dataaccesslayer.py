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
    products = Product.objects.all()
    return products

# gets all products that matches name
def get_all_products_by_name(name):
    products = Product.objects.filter(product_name = name)
    return products

def get_product_by_id(id):
    p = Product.objects.get(id = id)
    return p

def make_product_photo(url, product):
    photo = ProductPhoto(photo_url = url, photo_related_product = product)
    photo.save()
    return photo

def delete_product_photo(photo):
    photo.delete()
    return

def delete_product_photo_by_id(photo_id):
    photo = ProductPhoto.objects.get(id = photo_id)
    photo.delete()
    return

def get_product_photo_by_id(photo_id):
    photo = ProductPhoto.objects.get(id = photo_id)
    return photo

def get_product_photo_by_url(url):
    photo = ProductPhoto.objects.get(photo_url = url)
    return photo

def get_all_product_photos():
    product_photos = ProductPhoto.objects.all()
    return product_photos

def get_all_product_photos_by_product(product):
    photos = ProductPhoto.objects.filter(photo_related_product = product)
    return photos
