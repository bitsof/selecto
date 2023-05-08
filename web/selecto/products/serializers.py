from rest_framework import serializers
from products.models import Product, ProductPhoto, Review
from rest_framework import permissions
from django.contrib.auth.models import User

'''
The ModelSerializer class handles a lot of boilerplating, including:
    - generating an automatically determined set of fields
    - simple default implementations for  the create() and update() methods
'''
class ProductSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    class Meta:
        # choose the model product from products.models
        model = Product
        # select fields from the model description
        fields = ['pk', 'product_name', 'product_description']

class ReviewSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        # choose the model review from products.models
        model = Review
        # select fields from the model description
        fields = ['pk', 'review_related_product', 'review_content', 'review_publish_date']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username']