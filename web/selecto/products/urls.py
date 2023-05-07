from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import SignUpView

app_name = 'products'
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.ProductListView.as_view(), name='index'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='details'),
    path('products/<int:product_id>/reviews/<int:review_id>/', views.review_details, name='review_details'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us/', views.about_us, name='about_us'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
