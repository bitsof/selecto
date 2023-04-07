from django.contrib import admin

# Register your models here.

from .models import Product, Review, ProductPhoto, Store, StoreLink

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ProductPhoto)
admin.site.register(Store)
admin.site.register(StoreLink)
