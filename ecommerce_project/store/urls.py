from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('about/', views.about, name='about'),

    path('login/', views.user_login, name='login'),

    path('register/', views.register, name='register'),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'order/<int:product_id>/',
        views.order_now,
        name='order_now'
    ),

    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'buy-now/<int:product_id>/',
        views.buy_now,
        name='buy_now'
    ),
]