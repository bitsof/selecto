import pytest
from django.urls import reverse
import config
from dataaccesslayer import make_product, delete_product, delete_product_by_id, get_all_products, get_all_products_by_name, get_product_by_id
from products.models import Product

@pytest.mark.django_db
class TestDataAccess:
    def test_make_product(self):
        # Arrange
        name = "Test Product"
        description = "Test Description"
        # Act
        product = make_product(name, description)
        # Assert
        assert product.product_name == name
        assert product.product_description == description

    def test_delete_product(self):
        # Arrange
        name = "Test Product"
        description = "Test Description"
        product = make_product(name, description)
        # Act
        delete_product(product)
        # Assert
        assert not Product.objects.filter(id=product.id).exists()

    def test_delete_product_by_id(self):
        # Arrange
        name = "Test Product"
        description = "Test Description"
        product = make_product(name, description)
        # Act
        delete_product_by_id(product.id)
        # Assert
        assert not Product.objects.filter(id=product.id).exists()

    def test_get_all_products(self):
        # Arrange
        name1 = "Product 1"
        description1 = "Description 1"
        make_product(name1, description1)
        name2 = "Product 2"
        description2 = "Description 2"
        make_product(name2, description2)
        # Act
        products = get_all_products()
        # Assert
        assert len(products) == 2
        assert products[0].product_name == name1
        assert products[0].product_description == description1
        assert products[1].product_name == name2
        assert products[1].product_description == description2

    def test_get_all_products_by_name(self):
        # Arrange
        name1 = "Test Product"
        description1 = "Description 1"
        make_product(name1, description1)
        name2 = "Test Product"
        description2 = "Description 2"
        make_product(name2, description2)
        # Act
        products = get_all_products_by_name(name1)
        # Assert
        assert len(products) == 2
        assert products[0].product_name == name1
        assert products[0].product_description == description1
        assert products[1].product_name == name2
        assert products[1].product_description == description2

    def test_get_product_by_id(self):
        # Arrange
        name = "Test Product"
        description = "Test Description"
        product = make_product(name, description)
        # Act
        retrieved_product = get_product_by_id(product.id)
        # Assert
        assert retrieved_product == product