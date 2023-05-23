import pytest
from django.urls import reverse
import config
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.models import User
from products.models import Product, Review
import pytz
import re

@pytest.fixture
def product():
    data = {
        'product_name': 'Test Product',
        'product_description': 'This is a test product',
    }
    return Product.objects.create(**data)

@pytest.fixture
def review(product):
    time = timezone.now()
    data = {
        'review_related_product': product,
        'review_content': 'This is a test review',
        'review_publish_date' : time
    }
    return Review.objects.create(**data)

@pytest.fixture
def superuser():
    # Create a new superuser
    superuser = User(username="superuser", password="password123", is_superuser=True, is_staff=True)
    # Add the superuser to your database or user management system
    superuser.save()
    # Return the superuser object
    yield superuser
    # Remove the superuser from your database or user management system (if necessary)
    superuser.delete()

@pytest.fixture
def user():
    user = User(username="user", password="password123")
    user.save()
    yield user
    user.delete()

@pytest.mark.django_db
class TestApi:
    def test_api_product_list_get(self, client):
        url = reverse('products:api_product_list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_api_product_list_post_with_permission_superuser(self, client, superuser):
        url = reverse('products:api_product_list')
        data = {
            'product_name': 'Test Product',
            'product_description': 'This is a test product',
        }
        client.force_login(superuser)
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['product_name'] == data['product_name']
        assert response.data['product_description'] == data['product_description']

    def test_api_product_list_post_without_permission(self, client):
        url = reverse('products:api_product_list')
        data = {
            'product_name': 'Test Product',
            'product_description': 'This is a test product',
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_api_product_list_post_without_permission_user(self, client, user):
        url = reverse('products:api_product_list')
        data = {
            'product_name': 'Test Product',
            'product_description': 'This is a test product',
        }
        client.force_login(user)
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_product_details_get(self, client, product):
        url = reverse('products:api_product_details', kwargs={'pk': product.pk})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'Test Product' in response.data['product_name']

    def test_api_product_details_put_with_permission_superuser(self, client, product, superuser):
        url = reverse('products:api_product_details', kwargs={'pk': product.pk})
        data = {
            'product_name': 'Updated Product',
            'product_description': 'This is an updated product',
        }
        client.force_login(superuser)
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['product_name'] == data['product_name']
        assert response.data['product_description'] == data['product_description']

    def test_api_product_details_put_without_permission(self, client, product):
        url = reverse('products:api_product_details', kwargs={'pk': product.pk})
        data = {
            'product_name': 'Updated Product',
            'product_description': 'This is an updated product',
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_product_details_put_without_permission_user(self, client, product, user):
        url = reverse('products:api_product_details', kwargs={'pk': product.pk})
        data = {
            'product_name': 'Updated Product',
            'product_description': 'This is an updated product',
        }
        client.force_login(user)
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_product_details_delete_with_permission_superuser(self, client, product, superuser):
        url = reverse('products:api_product_details', kwargs={'pk': product.pk})
        client.force_login(superuser)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_api_product_details_delete_without_permission(self, client, product):
        url = reverse('products:api_product_details', kwargs={'pk': product.pk})
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_product_details_delete_without_permission_user(self, client, product, user):
        url = reverse('products:api_product_details', kwargs={'pk': product.pk})
        client.force_login(user)
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_review_list_get(self, client):
        url = reverse('products:api_review_list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_api_review_list_post_with_permission_superuser(self, client, product, superuser):
        url = reverse('products:api_review_list')
        # changes timezone to match test website as well as removes microseconds
        # there is an error with how formatting is done that results in microseconds being rounded off in json
        pacific = pytz.timezone('US/Pacific')
        time = timezone.now().astimezone(pacific).replace(microsecond=0)
        data = {
            'review_related_product': reverse('products:api_product_details', args=[product.pk]),
            'review_content': 'This is a test review',
            'review_publish_date' : time
        }
        client.force_login(superuser)
        response = client.post(url, data, format='json')
        # The url is in the format of a hyperlink
        url = response.data['review_related_product']
        # This regular expression gets the final numeric sequence, i.e. the pk
        pk = re.findall(r'\d+', url)[-1]
        assert response.status_code == status.HTTP_201_CREATED
        assert product.pk == int(pk)
        assert response.data['review_content'] == data['review_content']
        assert response.data['review_publish_date'] == data['review_publish_date'].isoformat()

    def test_api_review_list_post_without_permission(self, client, product):
        url = reverse('products:api_review_list')
        pacific = pytz.timezone('US/Pacific')
        time = timezone.now().astimezone(pacific).replace(microsecond=0)
        data = {
            'review_related_product': reverse('products:api_product_details', args=[product.pk]),
            'review_content': 'This is a test review',
            'review_publish_date' : time
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_review_list_post_without_permission_user(self, client, product, user):
        url = reverse('products:api_review_list')
        # changes timezone to match test website as well as removes microseconds
        # there is an error with how formatting is done that results in microseconds being rounded off in json
        pacific = pytz.timezone('US/Pacific')
        time = timezone.now().astimezone(pacific).replace(microsecond=0)
        data = {
            'review_related_product': reverse('products:api_product_details', args=[product.pk]),
            'review_content': 'This is a test review',
            'review_publish_date' : time
        }
        client.force_login(user)
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
  
    def test_api_review_detail_get(self, client, product, review):
        url = reverse('products:api_review_details', kwargs={'pk': 1})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'test review' in response.data['review_content']

    def test_api_review_detail_put_with_permission_superuser(self, client, product, review, superuser):
        url = reverse('products:api_review_details', kwargs={'pk': review.pk})
        pacific = pytz.timezone('US/Pacific')
        time = timezone.now().astimezone(pacific).replace(microsecond=0)
        data = {
            'review_related_product': reverse('products:api_product_details', args=[product.pk]),
            'review_content': 'This is an updated review',
            'review_publish_date' : time,
        }
        client.force_login(superuser)
        response = client.put(url, data, format='json', content_type='application/json')
        # The url is in the format of a hyperlink
        url = response.data['review_related_product']
        # This regular expression gets the final numeric sequence, i.e. the pk
        pk = re.findall(r'\d+', url)[-1]
        assert response.status_code == status.HTTP_200_OK
        assert product.pk == int(pk)
        assert response.data['review_content'] == data['review_content']
        assert response.data['review_publish_date'] == data['review_publish_date'].isoformat()

    def test_api_review_detail_put_without_permission(self, client, product, review):
        url = reverse('products:api_review_details', kwargs={'pk': review.pk})
        pacific = pytz.timezone('US/Pacific')
        time = timezone.now().astimezone(pacific).replace(microsecond=0)
        data = {
            'review_related_product': reverse('products:api_product_details', args=[product.pk]),
            'review_content': 'This is an updated review',
            'review_publish_date' : time,
        }
        response = client.put(url, data, format='json', content_type='application/json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_review_detail_put_without_permission_user(self, client, product, review, user):
        url = reverse('products:api_review_details', kwargs={'pk': review.pk})
        pacific = pytz.timezone('US/Pacific')
        time = timezone.now().astimezone(pacific).replace(microsecond=0)
        data = {
            'review_related_product': reverse('products:api_product_details', args=[product.pk]),
            'review_content': 'This is an updated review',
            'review_publish_date' : time,
        }
        client.force_login(user)
        response = client.put(url, data, format='json', content_type='application/json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_review_detail_delete_with_permission_superuser(self, client, product, review, superuser):
        url = reverse('products:api_review_details', kwargs={'pk': review.pk})
        client.force_login(superuser)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_api_review_detail_delete_without_permission(self, client, product, review):
        url = reverse('products:api_review_details', kwargs={'pk': review.pk})
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_review_detail_delete_without_permission_user(self, client, product, review, user):
        url = reverse('products:api_review_details', kwargs={'pk': review.pk})
        client.force_login(user)
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_user_list_get_with_permission_superuser(self, client, user, superuser):
        url = reverse('products:api_user_list')
        client.force_login(superuser)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_api_user_list_get_without_permission(self, client):
        url = reverse('products:api_user_list')
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_user_list_get_without_permission_user(self, client, user):
        url = reverse('products:api_user_list')
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_user_details_get_with_permission_superuser(self, client, user, superuser):
        url = reverse('products:api_user_details', kwargs={'pk': user.pk})
        client.force_login(superuser)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_api_user_details_get_without_permission(self, client, user):
        url = reverse('products:api_user_details', kwargs={'pk': user.pk})
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_api_user_details_get_without_permission_user(self, client, user):
        url = reverse('products:api_user_details', kwargs={'pk': user.pk})
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN