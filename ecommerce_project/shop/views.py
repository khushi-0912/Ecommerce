from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from .models import UserAccount

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_products_from_file():
    with open(settings.BASE_DIR / 'shop/products.json', 'r') as f:
        products = json.load(f)
    return products



def login_view(request):
    return render(request, 'shop/login.html')


def signup_view(request):
    return render(request, 'shop/signup.html')

def products_view(request):
    with open(os.path.join(BASE_DIR, 'shop', 'products.json')) as f:
        products = json.load(f)
    return render(request, 'shop/products.html', {'products': products})

def cart_view(request):
    cart = request.session.get('cart', [])
    
    products = get_products_from_file()
    
    product_dict = {product['id']: product for product in products}
    
    total = 0
    cart_details = []
    for item in cart:
        product_id = item['id']
        quantity = item['quantity']
        print(f"Product ID: {product_id}, Quantity: {quantity}")
        
        product = product_dict.get(int(product_id))
        print(f"Product: {product}")
        if product:
            product_total = product['price'] * quantity
            total += product_total
            cart_details.append({**product, 'quantity': quantity, 'total': product_total})
    
    total = round(total, 2) 
    return render(request, 'shop/cart.html', {'cart': cart_details, 'total': total})



def checkout(request):
    return redirect('thankyou')

def thankyou(request):
    cart = request.session.get('cart', [])
    
    products = get_products_from_file()
    
    product_dict = {product['id']: product for product in products}
    
    total = 0
    cart_details = []
    for item in cart:
        product_id = item['id']
        quantity = item['quantity']
        print(f"Product ID: {product_id}, Quantity: {quantity}")
        
        product = product_dict.get(int(product_id))
        print(f"Product: {product}")
        if product:
            product_total = product['price'] * quantity
            total += product_total
            cart_details.append({**product, 'quantity': quantity, 'total': round(product_total, 2)})

    total = round(total, 2)

    return render(request, 'shop/thankyou.html', {'cart': cart_details, 'total': total})

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            print(cart)
            request.session['cart'] = cart
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)


def get_total_quantity(request):
    cart = request.session.get('cart', [])
    total_quantity = 0
    for item in cart:
        total_quantity += int(item['quantity'])
    return JsonResponse({'quantity':total_quantity})



@csrf_exempt
def signup_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone_number = data.get('phone_number')

        if not (name and email and password and phone_number):
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        if UserAccount.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered.'}, status=400)

        user = UserAccount(
            name=name,
            email=email,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save()

        return JsonResponse({'message': 'Signup successful.'})

    return JsonResponse({'error': 'Invalid request.'}, status=400)


@csrf_exempt
def login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserAccount.objects.get(email=email)
            if user.check_password(password):
                return JsonResponse({'message': 'Login successful.'})
            else:
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)

    return JsonResponse({'error': 'Invalid request.'}, status=400)


def checkout(request):
    return render(request, 'shop/checkout.html')


def payment(request):
    if request.method == 'POST':
        return redirect('thankyou')
    return redirect('checkout')  