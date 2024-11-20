from django.contrib import admin
from .models import Product, Category
from rangefilter.filters import NumericRangeFilter


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']
    search_fields = ['name']
    list_filter = (('price', NumericRangeFilter),('stock', NumericRangeFilter),)