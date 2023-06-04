import pytest
from django.urls import reverse
import config
from dataaccesslayer import make_product
from products.models import Product, Review
from django.utils import timezone
from rest_framework import status

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
def test_home(client):
    url = reverse("products:home")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_index(client):
    url = reverse("products:index")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_details_view(client):
    product = make_product('Test Product', 'This is a test product.')
    url = reverse('products:details', args=[product.pk])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.context['product'] == product

@pytest.mark.django_db
def test_review_list_view(client, product, review):
    url = reverse('products:review_list', args=[product.pk])
    response = client.get(url)
    # Check that the response has a status code of 200 OK
    assert response.status_code == status.HTTP_200_OK
    # Check that the returned product_id matches the expected product.pk
    assert response.context['product_id'] == product.pk
    # Check that the returned review(s) belong to the correct product
    review_list = response.context['review_list']
    for review_obj in review_list:
        assert review_obj.review_related_product == product

@pytest.mark.django_db
def test_review_details_view(client):
    product = make_product('Test Product', 'This is a test product.')
    review = Review.objects.create(review_related_product=product, review_publish_date=timezone.now(), review_content='This is a test review.')
    url = reverse('products:review_details', args=[product.id, review.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.context['review'] == review