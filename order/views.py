from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from product.models import Product
from .forms import OrderRegisterForm
from .models import Order, OrderItem

# Create your views here.

@login_required(login_url='login')
def add_to_cart_view(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', {})

    current_quantity = cart[str(product_id)]['quantity'] if str(product_id) in cart else 0
    
    if product.stock > current_quantity:
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                'name': product.name,
                'price': product.price,
                'image_url': product.image.url if product.image else None,
                'quantity': 1,
            }
        request.session['cart'] = cart
    else:
        messages.error(request, 'موجودی کافی از این کالا وجود ندارد.')
    referer = request.META.get('HTTP_REFERER', 'default_redirect')
    return redirect(referer if referer else 'product')

@login_required(login_url='login')
def sub_from_cart_view(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)]['quantity'] == 1:
            del cart[str(product_id)]
        else:
            cart[str(product_id)]['quantity'] -= 1
    request.session['cart'] = cart
    referer = request.META.get('HTTP_REFERER', 'default_redirect')
    return redirect(referer if referer else 'product')

@login_required(login_url='login')
def del_from_cart_view(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    referer = request.META.get('HTTP_REFERER', 'default_redirect')
    return redirect(referer if referer else 'product')

@login_required(login_url='login')
def order_register_view(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    if not cart:
        messages.error(request, 'سبد خرید شما خالی است')

    if request.method == 'POST':
        form = OrderRegisterForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item_id, item in cart.items():
                product = Product.objects.get(id=item_id)
                order_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    unit_price=item['price']
                )
                order_item.save()
            
            request.session['cart'] = {}
            
            return redirect('pay', order_id=order.id)
    else:
        form = OrderRegisterForm()
    
    context = {
        'form': form,
        'cart': cart,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


@login_required(login_url='login')
def pay_view(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {
        'order': order
    }
    return render(request, 'pay.html', context)

def change_status_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    with transaction.atomic():
        order.status = 'Paid'
        order.save()
        
        for item in order.items.all():
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
            else:
                messages.error(request, f'موجودی کافی برای محصول {product.name} وجود ندارد.')
                return redirect('cart', order_id=order_id)

    return render(request, 'SuccessfulPay.html', {'order': order})

@login_required(login_url='login')
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)

@login_required(login_url='login')
def delete_order_view(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status == 'Pending':
        order.delete()
    return redirect('orders')

@login_required(login_url='login')
def order_detail_view(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {
        'order': order
    }
    return render(request, 'order_detail.html', context)