from django.db import models
from django.conf import settings
from product.models import Product

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total_price = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = [
        ('Pending', 'در انتظار پرداخت'),
        ('Paid', 'پرداخت شده'),
        ('Shipped', 'در حال ارسال'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    def update_total_price(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total_price = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_total_price()
