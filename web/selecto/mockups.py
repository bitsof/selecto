import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selecto.settings')
import django
django.setup()
import sys

from products.models import Product, Review

"""
Guide on adding entries through either python shell or python file courtesy of chatGPT:
Import the relevant models by typing from myapp.models import MyModel where myapp is the name of your app 
and MyModel is the name of the model you want to add data to.
Create a new instance of the model by typing my_model = MyModel(field1='value1', field2='value2'), 
where field1 and field2 are the names of the fields in your model 
and 'value1' and 'value2' are the values you want to assign to those fields.
Save the instance to the database by typing my_model.save().

Btw:
For every field that cannot be NULL, i.e. doesn't explicitly have null=True in its database declaration
in the model folder, there must be an argument setting it to some value.

Alternatively you can run the server, and just go to whatever the port is (probably http://127.0.0.1:8000/admin)
input the admin credentials and then there are options to add and delete entries in the tables. 
"""

def generate():
    description = "A tri-pod with a head that is designed to have smooth movement with pans."
    name = "Fluid head tri-pod"
    p = Product(product_description = description, product_name = name)
    p.save()
    products = Product.objects.all()

    reviews = ["The \"Fluid head tripod\" seems to be a great product for those looking for a sturdy and reliable tripod with smooth movement. The fluid head design ensures smooth panning, allowing for professional-level camera movements, and the tripod itself is built to be stable and durable." \

        "One of the key features of this product is the fluid head design, which makes it easy to create smooth and seamless camera movements. This is a great feature for anyone who needs to capture video or images with a professional look and feel." \

        "In addition to the fluid head, the tripod itself is well-built and designed for stability. It can easily support heavy cameras and lenses, and it is durable enough to withstand frequent use and travel." \

        "Overall, if you're in the market for a reliable tripod with smooth movement, the Fluid Head Tripod is definitely worth considering. Its high-quality construction and professional-grade features make it a great choice for photographers and videographers alike."]
    
    for r in reviews:
        entry = Review(review_content = r, review_related_product = p)
        entry.save()
    products = Product.objects.all()

# deletes all entries
def delete_all():
    products = Product.objects.all()
    # deletes all reviews as well, because of setting on_delete=models.CASCADE in the models file
    for p in products:
        p.delete()

# example more than anything useful
def get_product(id):
    p = Product.objects.get(id = id)
    print(p)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        globals()[sys.argv[1]]()
    elif len(sys.argv) == 3:
        globals()[sys.argv[1]](sys.argv[2])