## Accessing and Using the API

The API you've set up using Django REST Framework provides endpoints for managing products, reviews, and users. In this guide, we'll cover the basic operations you can perform on the API using various HTTP methods.

### Base URL

The base URL for accessing the API is `http://selecto.pro/api/` or if run locally `http://127.0.0.1:8000/api/`

### Authentication

Some API endpoints require admin-level authentication (within the user class, there is a boolean is_staff that it checks for), while others are read-only and accessible without authentication. 

If it is a development branch being run locally, you can run this command from the root directory
```shell
python .\web\selecto\manage.py createsuperuser
```
to create a user with that authentication. 

When creating a user outside of that command, such as in python, make sure to set is_staff=True.
```python
user = User(username="superuser", password="password123", is_superuser=True, is_staff=True)
user.save()
``` 

For authenticated endpoints, you need to include the appropriate authentication credentials in the request headers. Refer to the documentation or contact the API administrator for details on authentication requirements.

### Products

#### Retrieve All Products

- **Endpoint:** `GET /products/`
- **Description:** Retrieves a list of all products.
- **Authentication Required:** No

#### Retrieve a Single Product

- **Endpoint:** `GET /products/{product_id}/`
- **Description:** Retrieves details of a specific product.
- **Authentication Required:** No

#### Create a New Product

- **Endpoint:** `POST /products/`
- **Description:** Creates a new product.
- **Authentication Required:** Yes

#### Update a Product

- **Endpoint:** `PUT /products/{product_id}/`
- **Description:** Updates an existing product.
- **Authentication Required:** Yes

#### Delete a Product

- **Endpoint:** `DELETE /products/{product_id}/`
- **Description:** Deletes an existing product.
- **Authentication Required:** Yes

### Reviews

#### Retrieve All Reviews

- **Endpoint:** `GET /reviews/`
- **Description:** Retrieves a list of all reviews.
- **Authentication Required:** No

#### Retrieve a Single Review

- **Endpoint:** `GET /reviews/{review_id}/`
- **Description:** Retrieves details of a specific review.
- **Authentication Required:** No

#### Create a New Review

- **Endpoint:** `POST /reviews/`
- **Description:** Creates a new review.
- **Authentication Required:** Yes

#### Update a Review

- **Endpoint:** `PUT /reviews/{review_id}/`
- **Description:** Updates an existing review.
- **Authentication Required:** Yes

#### Delete a Review

- **Endpoint:** `DELETE /reviews/{review_id}/`
- **Description:** Deletes an existing review.
- **Authentication Required:** Yes

### Users

#### Retrieve All Users

- **Endpoint:** `GET /users/`
- **Description:** Retrieves a list of all users.
- **Authentication Required:** Yes

#### Retrieve a Single User

- **Endpoint:** `GET /users/{user_id}/`
- **Description:** Retrieves details of a specific user.
- **Authentication Required:** Yes

### Making API Requests

To interact with the API, you can use various HTTP clients, such as cURL, Postman, HTTPIE, or Python's `requests` library. Here's an example using `requests` in Python for a locally running server:

```python
import requests

# Set the base URL
base_url = 'http://127.0.0.1:8000/api/'

# Make a GET request to retrieve all products
response = requests.get(base_url + 'products/')
print(response.json())  # Process the response data as needed

# Make a POST request to create a new product
data = {
    'product_name': 'New Product',
    'product_description': 'This is a new product.'
}
username='username'
password='password'
response = requests.post(base_url + 'products/', json=data, auth=(username, password))
print(response.status_code)  # Check the response status code
```