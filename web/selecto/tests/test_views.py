import pytest
from django.urls import reverse
import config
from dataaccesslayer import make_product
from products.models import Review
from django.utils import timezone
from rest_framework import status

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
def test_review_details_view(client):
    product = make_product('Test Product', 'This is a test product.')
    review = Review.objects.create(review_related_product=product, review_publish_date=timezone.now(), review_content='This is a test review.')
    url = reverse('products:review_details', args=[product.id, review.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.context['review'] == review