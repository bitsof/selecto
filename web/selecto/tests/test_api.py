import pytest
from django.urls import reverse
import config
from rest_framework import status
from django.utils import timezone
from products.models import Product, Review
import pytz

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

@pytest.mark.django_db
class TestApi:
    def test_api_product_list_get(self, client):
        url = reverse('products:api-product-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_api_product_list_post(self, client):
        url = reverse('products:api-product-list')
        data = {
            'product_name': 'Test Product',
            'product_description': 'This is a test product',
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['product_name'] == data['product_name']
        assert response.data['product_description'] == data['product_description']

    def test_api_product_detail_get(self, client, product):
        url = reverse('products:api-product-details', kwargs={'pk': product.pk})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'Test Product' in response.data['product_name']

    def test_api_product_detail_put(self, client, product):
        url = reverse('products:api-product-details', kwargs={'pk': product.pk})
        data = {
            'product_name': 'Updated Product',
            'product_description': 'This is an updated product',
        }
        response = client.put(url, data, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['product_name'] == data['product_name']
        assert response.data['product_description'] == data['product_description']

    def test_api_product_detail_delete(self, client, product):
        url = reverse('products:api-product-details', kwargs={'pk': product.pk})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_api_review_list_get(self, client):
        url = reverse('products:api-review-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_api_review_list_post(self, client, product):
        url = reverse('products:api-review-list')
        pacific = pytz.timezone('US/Pacific')
        time = timezone.now().astimezone(pacific).replace(microsecond=0)
        data = {
            'review_related_product': product.pk,
            'review_content': 'This is a test review',
            'review_publish_date' : time
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['review_related_product'] == data['review_related_product']
        assert response.data['review_content'] == data['review_content']
        assert response.data['review_publish_date'] == data['review_publish_date'].isoformat()
            
    def test_api_review_detail_get(self, client, product, review):
        url = reverse('products:api-review-details', kwargs={'pk': 1})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'test review' in response.data['review_content']

    def test_api_review_detail_put(self, client, product, review):
        url = reverse('products:api-review-details', kwargs={'pk': review.pk})
        pacific = pytz.timezone('US/Pacific')
        time = timezone.now().astimezone(pacific).replace(microsecond=0)
        data = {
            'review_related_product': review.review_related_product.pk,
            'review_content': 'This is an updated review',
            'review_publish_date' : time,
        }
        response = client.put(url, data, format='json', content_type='application/json')
        print(data['review_publish_date'])
        assert response.status_code == status.HTTP_200_OK
        assert response.data['review_related_product'] == data['review_related_product']
        assert response.data['review_content'] == data['review_content']
        assert response.data['review_publish_date'] == data['review_publish_date'].isoformat()

    def test_api_review_detail_delete(self, client):
        url = reverse('products:api-review-details', kwargs={'pk': 1})