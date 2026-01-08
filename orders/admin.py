from django.contrib import admin
from .models import Order, OrderItem, Invoice

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['variant']
    extra = 0

class InvoiceInline(admin.StackedInline):
    model = Invoice
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'full_name', 'email', 'status', 'is_paid', 'created_at', 'get_total_price']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['tracking_id', 'full_name', 'email', 'phone_number']
    inlines = [OrderItemInline, InvoiceInline]
    readonly_fields = ['tracking_id', 'created_at']
    
    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['order', 'pdf_file', 'created_at']
    search_fields = ['order__tracking_id', 'order__full_name']
