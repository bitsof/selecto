import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_example(client):
    url = reverse("products:home")
    response = client.get(url)
    assert response.status_code == 200
