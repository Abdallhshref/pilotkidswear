from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import ProductVariant
from .models import OrderItem, Order
from .cart import Cart
from .forms import OrderCreateForm, OrderTrackingForm
from decimal import Decimal

@require_POST
def cart_add(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    # Get quantity from POST, default to 1 if not provided or invalid
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
        
    cart.add(variant=variant, quantity=quantity)
    return redirect('cart_detail')

def cart_remove(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.remove(variant)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('home')

    form = OrderCreateForm(request.POST or None)
    shipping_price = Decimal('0')
    discount_amount = Decimal('0')
    total_price = cart.get_total_price()

    if request.method == 'POST':
        # Check if user clicked "Update" or "Place Order"
        is_final_submit = 'place_order' in request.POST
        
        # Get city and coupon even if form isn't fully valid yet for preview
        city = request.POST.get('city')
        coupon_code = request.POST.get('coupon_code')

        # 1. Shipping Price Logic
        if city:
            if city in ['Cairo', 'Giza']:
                shipping_price = Decimal('50')
            else:
                shipping_price = Decimal('75')
        
        # 2. Discount Logic
        items_total = cart.get_total_price()
        if coupon_code == 'SAVE10':
            discount_amount = items_total * Decimal('0.10')
        
        # 3. Final Total Calculation for preview
        total_price = items_total + shipping_price - discount_amount

        if is_final_submit and form.is_valid():
            order = form.save(commit=False)
            order.shipping_price = shipping_price
            order.discount_amount = discount_amount
            order.total_price = total_price
            order.is_paid = False 
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    variant=item['variant'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                
                # Deduct Stock
                variant = item['variant']
                stock = variant.stocks.first()
                if stock:
                    stock.quantity -= item['quantity']
                    stock.save()

            cart.clear()
            return redirect('order_created', order_id=order.tracking_id)
    
    context = {
        'cart': cart,
        'form': form,
        'shipping_price': shipping_price,
        'discount_amount': discount_amount,
        'total_price': total_price
    }
    return render(request, 'orders/checkout.html', context)

def order_created(request, order_id):
    order = get_object_or_404(Order, tracking_id=order_id)
    # Calculate subtotal (sum of items) for display
    subtotal = sum(item.get_cost() for item in order.items.all())
    return render(request, 'orders/created.html', {'order': order, 'subtotal': subtotal})

def track_order(request):
    order = None
    form = OrderTrackingForm(request.GET or None)
    
    if form.is_valid():
        tracking_id = form.cleaned_data['tracking_id']
        try:
            order = Order.objects.get(tracking_id=tracking_id)
        except Order.DoesNotExist:
            form.add_error('tracking_id', "Order not found")

    return render(request, 'orders/track_order.html', {'form': form, 'order': order})

def download_invoice(request, order_id):
    # Placeholder for invoice download
    return redirect('order_created', order_id=order_id)

def resend_invoice(request, order_id):
    # Placeholder for resending invoice
    return redirect('order_created', order_id=order_id)
