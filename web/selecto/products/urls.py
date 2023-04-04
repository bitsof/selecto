from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>/', views.details, name='details'),
    path('<int:product_id>/<int:review_id>/', views.review_details, name='review_details'),
]
