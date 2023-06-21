from django.contrib import admin
from django.forms import ModelForm, DateTimeInput, DateTimeField

# Register your models here.

from .models import Product, Review, ProductPhoto, Store, StoreLink, SelectoUser

admin.site.register(Product)

# Custom form for the Review model
class ReviewModelForm(ModelForm):
    # the 'datetime-local' is an input type attribute for HTML
    # it is what allows the little calendar and clock to appear
    review_publish_date = DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Review
        # all fields are included, as opposed to some
        fields = '__all__'

# Registering the Review model with the custom form in the admin site
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewModelForm

admin.site.register(ProductPhoto)
admin.site.register(Store)
admin.site.register(StoreLink)
admin.site.register(SelectoUser)