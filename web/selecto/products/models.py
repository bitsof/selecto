from django.db import models

# Create your models here.

"""
Basic database setup. This is just code to tell Django how to initialize a SQLlite database.
Additionial information on fields, 
and options for fields here: https://docs.djangoproject.com/en/4.1/ref/models/fields/ 
"""

class Product(models.Model):
    product_description = models.CharField(max_length = 1000)
    product_name = models.CharField(max_length = 100)

class Review(models.Model):
    review_content = models.CharField(max_length=3000)
    review_related_product = models.ForeignKey(Product, on_delete=models.CASCADE)