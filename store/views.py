from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    return render(request, 'store/home.html', {'new_arrivals': new_arrivals})

import json

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get all variants with related color and size
    variants = product.variants.select_related('color', 'size').all()
    
    # Build data for JS
    # Structure: { color_id: { size_id: { variant_id: x, stock: y } } }
    variant_data = {}
    available_colors = set()
    available_sizes = set()

    for variant in variants:
        c_id = variant.color.id
        s_id = variant.size.id
        
        if c_id not in variant_data:
            variant_data[c_id] = {}
        
        # Check stock
        stock = variant.stocks.first()
        qty = stock.quantity if stock else 0
        
        variant_data[c_id][s_id] = {
            'variant_id': variant.id,
            'quantity': qty,
            'in_stock': qty > 0
        }
        
        available_colors.add(variant.color)
        available_sizes.add(variant.size)

    # Sort for display
    colors = sorted(list(available_colors), key=lambda c: c.name)
    sizes = sorted(list(available_sizes), key=lambda s: s.order)
    
    # Build color-to-image mapping
    color_images = {}
    for img in product.images.filter(color__isnull=False):
        if img.color_id not in color_images:
            color_images[img.color_id] = img.image.url
    
    # Default image for colors without specific images
    default_image = product.main_image.url if product.main_image else ''

    context = {
        'product': product,
        'variant_data_json': json.dumps(variant_data),
        'color_images_json': json.dumps(color_images),
        'default_image': default_image,
        'colors': colors,
        'sizes': sizes,
    }
    return render(request, 'store/product_detail.html', context)

def shop(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None

    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'store/shop.html', context)

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'store/shop.html', {'products': products, 'query': query})
