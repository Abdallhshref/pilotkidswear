from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid
from store.models import ProductVariant

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )

    GOVERNORATE_CHOICES = (
        ('Cairo', _('Cairo')),
        ('Giza', _('Giza')),
        ('Alexandria', _('Alexandria')),
        ('Dakahlia', _('Dakahlia')),
        ('Red Sea', _('Red Sea')),
        ('Beheira', _('Beheira')),
        ('Fayoum', _('Fayoum')),
        ('Gharbia', _('Gharbia')),
        ('Ismailia', _('Ismailia')),
        ('Monufia', _('Monufia')),
        ('Minya', _('Minya')),
        ('Qalyubia', _('Qalyubia')),
        ('New Valley', _('New Valley')),
        ('Suez', _('Suez')),
        ('Aswan', _('Aswan')),
        ('Assiut', _('Assiut')),
        ('Beni Suef', _('Beni Suef')),
        ('Port Said', _('Port Said')),
        ('Damietta', _('Damietta')),
        ('Sharkia', _('Sharkia')),
        ('South Sinai', _('South Sinai')),
        ('Kafr El Sheikh', _('Kafr El Sheikh')),
        ('Matrouh', _('Matrouh')),
        ('Luxor', _('Luxor')),
        ('Qena', _('Qena')),
        ('North Sinai', _('North Sinai')),
        ('Sohag', _('Sohag')),
    )

    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100, choices=GOVERNORATE_CHOICES)
    
    # Pricing fields
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Simple payment tracking
    is_paid = models.BooleanField(default=False)
    payment_metadata = models.JSONField(default=dict, blank=True) # For Paymob response

    def __str__(self):
        return f"Order {self.tracking_id} - {self.full_name}"

    def get_total_price(self):
        items_total = sum(item.get_cost() for item in self.items.all())
        return items_total + self.shipping_price - self.discount_amount

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Snapshot of price at time of order
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.variant}"

    def get_cost(self):
        return self.price * self.quantity

class Invoice(models.Model):
    order = models.OneToOneField(Order, related_name='invoice', on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.order.tracking_id}"
