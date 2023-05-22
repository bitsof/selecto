from django.db import models

# Create your models here.

"""
Basic database setup. This is just code to tell Django how to initialize a SQLlite database.
Additionial information on fields, 
and options for fields here: https://docs.djangoproject.com/en/4.1/ref/models/fields/ 
"""

class Product(models.Model):
    product_name = models.CharField(max_length = 100)
    product_description = models.CharField(max_length =30000)

    #defines how the string is formatted on the admin page
    def __str__(self):
        return f"{self.product_name} ({self.pk})"

    # defines meta class with field ordering required for restframework to know how to order items listed in API
    class Meta:
        ordering = ['product_name']

class Review(models.Model):
    review_content = models.CharField(max_length=3000)
    review_related_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_publish_date = models.DateTimeField()

    class Meta:
        # orders by the primary key
        ordering = ['pk']

class ProductPhoto(models.Model):
    photo_url = models.URLField()
    photo_related_product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        # orders by the primary key
        ordering = ['pk']

class Store(models.Model):
    store_name = models.CharField(max_length = 200)
    store_url_home = models.URLField()

    #defines how the string is formatted on the admin page
    def __str__(self):
        return f"{self.store_name} ({self.pk})"

    class Meta:
        ordering = ['store_name']

class StoreLink(models.Model):
    store_link_url = models.URLField()
    store_link_related_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store_link_store =  models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        # orders by the primary key
        ordering = ['pk']


