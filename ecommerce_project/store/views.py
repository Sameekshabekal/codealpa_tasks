from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from .models import Product,Order, OrderItem


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def about(request):
    return render(request, 'store/about.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect('home')

        return render(
            request,
            'store/login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'store/login.html')


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(
        request,
        'store/product_detail.html',
        {'product': product}
    )


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'store/register.html',
                {'error': 'Username already exists.'}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'store/register.html')




def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def cart(request):
    cart_data = request.session.get('cart', {})

    items = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(Product, id=product_id)

        item_total = product.price * quantity
        total += item_total

        items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
        })

    return render(
        request,
        'store/cart.html',
        {
            'items': items,
            'total': total,
        }
    )


def checkout(request):
    cart_data = request.session.get('cart', {})

    if not cart_data:
        return redirect('cart')

    items = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=product_id)

        item_total = product.price * quantity
        total += item_total

        items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
        })

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return redirect('login')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status='Pending'
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

            # Reduce product stock
            item['product'].stock -= item['quantity']
            item['product'].save()

        # Empty the cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_success', order_id=order.id)

    return render(
        request,
        'store/checkout.html',
        {
            'items': items,
            'total': total,
        }
    )


def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'store/order_success.html',
        {'order': order}
    )

def order_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Put only this product into the cart
    request.session['cart'] = {
        str(product_id): 1
    }
    request.session.modified = True

    return redirect('checkout')

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        return redirect('product_detail', product_id=product.id)

    # Create a temporary cart with only this product
    request.session['cart'] = {
        str(product.id): 1
    }
    request.session.modified = True

    # Go to checkout, but DON'T create the order yet
    return redirect('checkout')