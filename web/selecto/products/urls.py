from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'products'
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.ProductListView.as_view(), name='index'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='details'),
    path('products/<int:product_id>/reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_details'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us/', views.about_us, name='about_us'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/products/', views.ApiProductList.as_view(), name='api_product_list'),
    path('api/products/<int:pk>/', views.ApiProductDetail.as_view(), name='api_product_details'),
    path('api/reviews/', views.ApiReviewList.as_view(), name='api_review_list'),
    path('api/reviews/<int:pk>/', views.ApiReviewDetail.as_view(), name='api_review_details'),
    path('api/users/', views.UserList.as_view(), name='api_user_list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='api_user_details'),
    path('api/', views.api_root),
    path('signup/', views.signup, name='signup'),
]

urlpatterns = format_suffix_patterns(urlpatterns)