import dataaccesslayer
from products.models import Product, Review, ProductPhoto, Store, StoreLink 

print('Number of products: ', len(Product.objects.all()))
p = dataaccesslayer.make_product('Example', 'Example description')
print(p)
print('Number of products now: ', len(Product.objects.all()))
dataaccesslayer.delete_product(p)
print('Number of products now: ', len(Product.objects.all()))

for p in dataaccesslayer.get_all_products():
    dataaccesslayer.delete_product(p)