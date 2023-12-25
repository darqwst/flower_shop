from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerCreateSerializer
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from .models import WalletTransaction, Customer
from .forms import WalletTransactionForm
from django.db import transaction
import requests

def homeView(request):
    products = Product.objects.all()[:15]

    if 'cart' in request.session.keys():
        context = {
            'categories': Category.objects.all(),
            'cart': request.session['cart'],
            'products': products,
        }
    else:
        context = {
            'categories': Category.objects.all(),
            'products': products,
        }

    return render(request=request, template_name='home.html', context=context)

class CustomerCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthApiView(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: 'Добро пожаловать!',
            403: 'Username или пароль недействительны!',
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Полученный юзернэйм: {username}, пароль: {password}")

        user = authenticate(username=username, password=password)
        print(f"Пользователь: {user}")

        print("Попытка:", username, "Результат:", user)

        if user is not None and check_password(password, user.password):
            login(request, user)
            return redirect('home_url')
        else:
            data = {'message': 'Username или пароль недействительны!'}
            return Response(data, HTTP_403_FORBIDDEN)

    def get(self, request):
        return render(request, 'auth.html')


class RegistrationApiView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = CustomerCreateSerializer(data=request.data, partial=False)
        if serializer.is_valid():
            customer = serializer.save()
            print(f'Customer created: {customer.username}')

            try:
                token, created = Token.objects.get_or_create(user=customer.user)
                return redirect('auth_api_url')

            except User.DoesNotExist:
                print(f'Нет такого юзера: {customer.username}')

        return redirect('auth_api_url')

    def get(self, request):
        return render(request, 'registration.html')

def signOutView(request):
    logout(request)
    return redirect('home_url')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin, login_url='home_url')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_url')
    else:
        form = ProductForm()

    context = {
        'categories': Category.objects.all(),
        'form': form,
    }
    return render(request, 'add_product.html', context)

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'view_product.html', context)

@user_passes_test(is_admin, login_url='home_url')
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_url')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'update_product.html', context)

@user_passes_test(is_admin, login_url='home_url')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('products_url')

    context = {
        'product': product,
    }
    return render(request, 'delete_product.html', context)

def productsView(request):
    sort_by = request.GET.get('sort_by', 'price')
    order = request.GET.get('order', 'asc')

    products = Product.objects.all()

    if sort_by == 'price':
        products = products.order_by('price') if order == 'asc' else products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name') if order == 'asc' else products.order_by('-name')

    context = {
        'categories': Category.objects.all(),
        'products': products,
        'category': 'All Products'
    }
    return render(request=request, template_name='products.html', context=context)

def addToCartView(request, product_id):
    if 'cart' not in request.session.keys():
        request.session['cart'] = [product_id]
    else:
        request.session['cart'].append(product_id)
        request.session.modified = True

    return redirect('cart_detail_url')

def removeProductFromCartView(request, product_id):
    if 'cart' in request.session.keys():
        cart = request.session['cart']
        if product_id in cart:
            cart.remove(product_id)
            request.session.modified = True

    return redirect('cart_detail_url')

@transaction.atomic
def cartDetailView(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all(),
        }
        total = 0
        if 'cart' in request.session.keys():
            context['cart'] = []
            count = 1
            for product_id in request.session.get('cart', []):
                product = Product.objects.get(id=product_id)
                product.count = count
                context['cart'].append(product)
                count += 1
                total += product.price
        context['total'] = total
        return render(request=request, template_name='cart.html', context=context)
    elif request.method == 'POST':
        total = int(request.POST.get('total'))
        customer = request.user.customer

        if customer.wallet >= total:
            customer.wallet -= total
            customer.save()

            order = Order.objects.create(user=request.user, total_price=total)
            for product_id in request.session.get('cart', []):
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(order=order, product=product, quantity=1)
            request.session.pop('cart')

            return redirect('profile_url')
        else:
            context = {
                'categories': Category.objects.all(),
                'error': 'Balance on your Wallet is not enough!'
            }
            if 'cart' in request.session.keys():
                context['cart'] = []
                count = 1
                for product_id in request.session.get('cart', []):
                    product = Product.objects.get(id=product_id)
                    product.count = count
                    context['cart'].append(product)
                    count += 1
                context['total'] = total
            return render(request=request, template_name='cart.html', context=context)

def profileView(request):
    if request.user.is_authenticated:
        context = {
            'categories': Category.objects.all(),
            'user': request.user.customer,
        }
        return render(request=request, template_name='profile.html', context=context)
    return redirect('sign_in_url')

def profileEditView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomerUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile_url')
        else:
            form = CustomerUpdateForm(instance=request.user)

        context = {
            'categories': Category.objects.all(),
            'form': form
        }
        return render(request=request, template_name='profile_edit.html', context=context)
    return redirect('sign_in_url')

def profileDeleteView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.user.delete()
            return redirect('home_url')
        context = {
            'categories': Category.objects.all(),
        }
        return render(request=request, template_name='profile_delete.html', context=context)
    return redirect('sign_in_url')

def productsByCategoryView(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'categories': Category.objects.all(),
        'products': products,
        'category': category.name
    }
    return render(request=request, template_name='products.html', context=context)

def search_results_view(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
        context = {
            'results': results,
            'query': query,
        }
        return render(request, 'search_results.html', context)
    else:
        return redirect('products_url')

class RechargeWalletView(View):
    template_name = 'recharge_wallet.html'

    def get(self, request):
        form = WalletTransactionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = WalletTransactionForm(request.POST)

        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiration_date = form.cleaned_data['expiration_date']
            cvv = form.cleaned_data['cvv']
            amount = form.cleaned_data['amount']
            user = request.user
            try:
                customer = Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                messages.error(request, 'User has no customer.')
                return redirect('recharge_wallet_url')

            customer.wallet += amount
            customer.save()

            WalletTransaction.objects.create(
                user=user,
                card_number=card_number,
                expiration_date=expiration_date,
                cvv=cvv,
                amount=amount
            )

            messages.success(request, 'Wallet successfully recharged.')
            return redirect('profile_url')

        return render(request, self.template_name, {'form': form})


class ProcessPaymentView(View):
    template_name = 'process_payment.html'

    def post(self, request):
        form = PaymentForm(request.POST)

        if form.is_valid():
            total = form.cleaned_data['total']
            action = form.cleaned_data['action']
            user = request.user
            wallet_transaction = WalletTransaction.objects.create(
                user=user,
                amount=total
            )

            if user.customer.wallet >= total:
                user.customer.wallet -= total
                user.customer.save()
                order = Order.objects.create(
                    user=user,
                    total_price=total
                )
                user_order = Order.objects.get_or_create(user=user)[0]
                user_order.items.clear()

                messages.success(request, 'Payment successful. Order placed.')
                return redirect('profile_url')
            else:
                messages.error(request, 'Insufficient funds in your wallet.')
        return redirect('cart_detail_url')

class OrderHistoryView(View):
    template_name = 'order_history.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
        return render(request, self.template_name, {'orders': orders})


def get_location(request):
    try:
        ip_address = requests.get('https://api64.ipify.org?format=json').json()['ip']
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        data = response.json()
        context = {
            'ip_address': data['ip'],
            'location': f"{data['city']}, {data['region']}, {data['country']}",
            'latitude_longitude': data['loc']
        }

        return render(request, 'location.html', context)

    except Exception as e:
        return HttpResponse(f"Error: {e}")