from store.models import Product, Size

print("Sizes:", list(Size.objects.values_list('name', flat=True)))
print("Products starting with W/w:", list(Product.objects.filter(name__istartswith='w').values_list('name', flat=True)))
