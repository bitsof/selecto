from rest_framework import serializers
from products.models import Product, ProductPhoto, Review
from rest_framework import permissions
from django.contrib.auth.models import User
from .permissions import IsAdminOrReadOnly

'''
The ModelSerializer class handles a lot of boilerplating, including:
    - generating an automatically determined set of fields
    - simple default implementations for  the create() and update() methods
'''
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = [IsAdminOrReadOnly]
    
    class Meta:
        # choose the model product from products.models
        model = Product
        # select fields from the model description
        fields = ['pk', 'product_name', 'product_description']

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = [IsAdminOrReadOnly]
    '''
    While new fields can be defined here to display,
    Hyperlinkedrelatedfields require a field to be defined in the model.
    In this case it's review_related_product, and rather than list
    the primary key or pk for short, it lists a url linking to the
    corresponding products product detail page in the api.
    '''
    review_related_product = serializers.HyperlinkedRelatedField(view_name='products:api_product_details',
                                                  queryset=Product.objects.all())

    class Meta:
        # choose the model review from products.models
        model = Review
        # select fields from the model description to display
        fields = ['pk', 'review_related_product', 'review_content', 'review_publish_date']

class UserSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAdminUser]

    class Meta:
        model = User
        # select fields to display
        # refer to https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#user-model for additional fields
        fields = ['pk', 'username']