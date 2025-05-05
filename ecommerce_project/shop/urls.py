from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    # path('/login', views.login_view, name='login-2'),
    path('products/', views.products_view, name='products'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('thank-you/', views.thankyou, name='thankyou'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get-cart-quantity/', views.get_total_quantity, name='get_cart_quantity'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('api/signup/', views.signup_api, name='signup_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('payment/', views.payment, name='payment'),
]
