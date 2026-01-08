from django.core.management.base import BaseCommand
from store.models import Category, Product, Color, Size, ProductVariant, Store, Stock
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        # Categories
        cat_clothes, _ = Category.objects.get_or_create(name='Clothes', slug='clothes')
        cat_acc, _ = Category.objects.get_or_create(name='Accessories', slug='accessories')

        # Colors
        c_sage, _ = Color.objects.get_or_create(name='Sage Green', hex_code='#A8C3BC')
        c_red, _ = Color.objects.get_or_create(name='Rust Red', hex_code='#8B4513')
        c_beige, _ = Color.objects.get_or_create(name='Beige', hex_code='#F5F5DC')
        c_mustard, _ = Color.objects.get_or_create(name='Mustard Yellow', hex_code='#E1AD01')

        # Sizes
        s_03, _ = Size.objects.get_or_create(name='0-3M', order=1)
        s_36, _ = Size.objects.get_or_create(name='3-6M', order=2)
        s_69, _ = Size.objects.get_or_create(name='6-9M', order=3)

        # Products
        p1, _ = Product.objects.get_or_create(
            slug='organic-romper',
            defaults={
                'name': 'Unisex Organic Romper',
                'category': cat_clothes,
                'description': 'Soft organic cotton romper for your little one.',
                'base_price': 25.00,
                'main_image': 'products/romper.png'
            }
        )
        # Update image if it exists but wasn't set originally
        if p1.main_image != 'products/romper.png':
           p1.main_image = 'products/romper.png'
           p1.save()
        
        p2, _ = Product.objects.get_or_create(
            slug='bucket-hat',
            defaults={
                'name': 'Sun Bucket Hat',
                'category': cat_acc,
                'description': 'Protect your baby from the sun in style.',
                'base_price': 15.00,
                'main_image': 'products/hat.png'
            }
        )
        if p2.main_image != 'products/hat.png':
           p2.main_image = 'products/hat.png'
           p2.save()

        p3, _ = Product.objects.get_or_create(
            slug='knit-sweater',
            defaults={
                'name': 'Cozy Knit Sweater',
                'category': cat_clothes,
                'description': 'Warm and stylish knit sweater for easier seasons.',
                'base_price': 35.00,
                'main_image': 'products/sweater.png'
            }
        )
        if p3.main_image != 'products/sweater.png':
           p3.main_image = 'products/sweater.png'
           p3.save()

        # Variants
        v1, _ = ProductVariant.objects.get_or_create(product=p1, color=c_sage, size=s_03)
        v2, _ = ProductVariant.objects.get_or_create(product=p1, color=c_sage, size=s_36)
        v3, _ = ProductVariant.objects.get_or_create(product=p1, color=c_red, size=s_03)
        
        v4, _ = ProductVariant.objects.get_or_create(product=p2, color=c_beige, size=s_36)
        v5, _ = ProductVariant.objects.get_or_create(product=p2, color=c_sage, size=s_36)

        v6, _ = ProductVariant.objects.get_or_create(product=p3, color=c_mustard, size=s_03)
        v7, _ = ProductVariant.objects.get_or_create(product=p3, color=c_mustard, size=s_36)
        v8, _ = ProductVariant.objects.get_or_create(product=p3, color=c_mustard, size=s_69)

        # Store
        store_main, _ = Store.objects.get_or_create(name='Main Warehouse', address='123 Baby St')

        # Stock
        Stock.objects.update_or_create(store=store_main, variant=v1, defaults={'quantity': 15})
        Stock.objects.update_or_create(store=store_main, variant=v2, defaults={'quantity': 8})
        Stock.objects.update_or_create(store=store_main, variant=v3, defaults={'quantity': 0}) # Out of stock
        Stock.objects.update_or_create(store=store_main, variant=v4, defaults={'quantity': 20})
        Stock.objects.update_or_create(store=store_main, variant=v5, defaults={'quantity': 5})
        Stock.objects.update_or_create(store=store_main, variant=v6, defaults={'quantity': 10})
        Stock.objects.update_or_create(store=store_main, variant=v7, defaults={'quantity': 2}) # Low stock
        Stock.objects.update_or_create(store=store_main, variant=v8, defaults={'quantity': 12})
        
        # Gallery Images (Reusing existing images for demo)
        from store.models import ProductImage
        # Romper gets a detail shot (using same image for now or cross-sell)
        ProductImage.objects.get_or_create(product=p1, image='products/romper.png', alt_text='Front view')
        ProductImage.objects.get_or_create(product=p1, image='products/hat.png', alt_text='Styled with hat')
        
        # Sweater gets detail
        ProductImage.objects.get_or_create(product=p3, image='products/sweater.png', alt_text='Folded view')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with Images and Variants'))
