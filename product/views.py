from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def home_page(request):
    is_authenticated = request.user.is_authenticated
    is_admin = request.user.is_staff
    categorys = list(Category.objects.all())
    products = list(Product.objects.all())
    context = {
        'is_authenticated': is_authenticated,
        'is_admin': is_admin,
        'categorys': categorys,
        'products': products
    }
    return render(request, 'HomePage.html', context)

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    products = list(products)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'category.html', context)

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_in_cart = cart.get(str(product_id), {})
    quantity_in_cart = product_in_cart.get('quantity', 0)
    context = {
        'product': product,
        'in_cart': bool(product_in_cart),
        'quantity_in_cart': quantity_in_cart,
    }
    return render(request, 'product.html', context)

def search_view(request):
    name = request.GET.get('name')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')
    category_id = request.GET.get('category')

    products = Product.objects.all()

    if name and name != 'None':
        products = products.filter(name__icontains=name)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if in_stock is not None:
        if in_stock == 'true':
            products = products.filter(stock__gt=0)
        elif in_stock == 'false':
            products = products.filter(stock__lte=0)
    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'name': '' if name == 'None' else name,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'selected_category': category_id,
    }
    return render(request, 'search.html', context)
