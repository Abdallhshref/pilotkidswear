from django.test import TestCase, Client
from django.urls import reverse
from orders.models import Order, OrderItem
from store.models import Product, Category, ProductVariant, Color, Size, Store
from decimal import Decimal

class TrackingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(name='Prod', slug='prod', category=self.category, base_price=Decimal('100.00'), main_image='img.jpg')
        self.color = Color.objects.create(name='Red', hex_code='#F00')
        self.size = Size.objects.create(name='M')
        self.variant = ProductVariant.objects.create(product=self.product, color=self.color, size=self.size)
        
        self.order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            status='shipped'
        )
        OrderItem.objects.create(order=self.order, variant=self.variant, price=Decimal('100.00'), quantity=2)

    def test_tracking_page_renders(self):
        url = reverse('track_order') + f'?tracking_id={self.order.tracking_id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Status')
        self.assertContains(response, 'Shipped')
        self.assertContains(response, 'Prod')
        self.assertContains(response, 'Red / M')
