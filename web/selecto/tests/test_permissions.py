from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from products.permissions import IsAdminOrReadOnly
import pytest

factory = APIRequestFactory()

@pytest.mark.django_db
def test_is_admin_or_read_only_permission():
    # Create an instance of the permission class
    permission = IsAdminOrReadOnly()

    # Create a user (non-admin)
    user = User.objects.create_user(username='testuser', password='testpassword')

    # Create a request for a safe method (GET)
    request = factory.get('/example/')
    request.user = user

    # Assert that the permission allows access for safe methods
    assert permission.has_permission(request, user) is True

    # Create a request for a non-safe method (POST)
    request = factory.post('/example/')
    request.user = user

    # Assert that the permission denies access for non-safe methods for non-admin users
    assert permission.has_permission(request, user) is False

    # Make the user an admin
    user.is_staff = True
    user.save()

    # Assert that the permission allows access for non-safe methods for admin users
    assert permission.has_permission(request, None) is True
    user.delete()