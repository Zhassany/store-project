from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

@admin.register(Order)
class OrderRegister(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'order_date', 'shipping_address']
    search_fields = ['user', 'total_price', 'status', 'order_date', 'shipping_address']

@admin.register(OrderItem)
class OrderItemRegister(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    search_fields = ['order', 'product', 'quantity', 'unit_price']
