from django.urls import path
from .views import category_view, product_view

urlpatterns = [
    path('<int:category_id>/', category_view, name='category'),
    path('product/<int:product_id>/', product_view, name='product')
]
