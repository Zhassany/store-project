from django.urls import path
from .views import add_to_cart_view, sub_from_cart_view, del_from_cart_view, order_register_view, pay_view
from .views import change_status_view, orders_view, delete_order_view, order_detail_view

urlpatterns = [
    path('add_cart/<int:product_id>/', add_to_cart_view, name='add_cart'),
    path('sub_cart/<int:product_id>/', sub_from_cart_view, name='sub_cart'),
    path('del_cart/<int:product_id>/', del_from_cart_view, name='del_cart'),
    path('cart/', order_register_view, name='cart'),
    path('pay/<int:order_id>/', pay_view, name='pay'),
    path('change_status/<int:order_id>/', change_status_view, name='change_status'),
    path('orders/', orders_view, name='orders'),
    path('del_order/<int:order_id>/', delete_order_view, name='delete_order'),
    path('order_detail/<int:order_id>/', order_detail_view, name='order_detail')
]