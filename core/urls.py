from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('export/users/excel/', views.export_users_excel, name='export_users_excel'),
    path('export/users/csv/', views.export_users_csv, name='export_users_csv'),
    path('export/orders/excel/', views.export_orders_excel, name='export_orders_excel'),
    path('export/orders/csv/', views.export_orders_csv, name='export_orders_csv'),
]
