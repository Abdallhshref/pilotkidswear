from django.urls import path
from . import views

urlpatterns = [
    path('track/', views.track_order, name='track_order'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:variant_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:variant_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('created/<uuid:order_id>/', views.order_created, name='order_created'),
    path('invoice/<uuid:order_id>/', views.download_invoice, name='download_invoice'),
    path('resend-invoice/<uuid:order_id>/', views.resend_invoice, name='resend_invoice'),
]
