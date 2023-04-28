import pytest
from django.urls import reverse
import config

@pytest.mark.django_db
def test_home(client):
    url = reverse("products:home")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_index(client):
    url = reverse("products:index")
    response = client.get(url)
    assert response.status_code == 200
                          