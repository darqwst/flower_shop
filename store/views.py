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
        print(f"Received username: {username}, password: {password}")

        user = authenticate(username=username, password=password)
        print(f"Authenticated user: {user}")

        print("Attempting authentication for user:", username, "Result:", user)

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
                print(f'User does not exist for username: {customer.username}')

        return redirect('auth_api_url')

    def get(self, request):
        return render(request, 'registration.html')



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
    context = {
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
        'category': 'All Products'
    }
    return render(request=request, template_name='products.html', context=context)


def addToCartView(request, product_id):
    if 'cart' not in request.session.keys():
        request.session['cart'] = [product_id]
    else:
        request.session['cart'].append(product_id)
        request.session.modified = True
    return HttpResponse()

def removeProductFromCartView(request, product_id):
    if 'cart' in request.session.keys():
        cart = request.session['cart']
        if product_id in cart:
            cart.remove(product_id)
            request.session.modified = True

    return redirect('cart_detail_url')

def cartDetailView(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all(),
        }
        total = 0
        if 'cart' in request.session.keys():
            context['cart'] = []
            count = 1
            for product_id in request.session['cart']:
                product = Product.objects.get(id=product_id)
                product.count = count
                context['cart'].append(product)
                count += 1
                total += product.price
        context['total'] = total
        return render(request=request, template_name='cart.html', context=context)
    elif request.method == 'POST':
        total = int(request.POST.get('total'))
        if request.user.wallet >= total:
            request.user.wallet -= total
            request.user.save()
            request.session.pop('cart')
            return redirect('profile_url')
        else:
            context = {
                'categories': Category.objects.all(),
                'error': 'Balance on you Wallet is not enough!'
            }
            if 'cart' in request.session.keys():
                context['cart'] = []
                count = 1
                for product_id in request.session['cart']:
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
            'user': request.user
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

class WalletRechargeView(APIView):
    def get(self, request, *args, **kwargs):
        form = WalletRechargeForm()
        return render(request, 'recharge_wallet.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = WalletRechargeForm(request.data)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            card_cvv = form.cleaned_data['card_cvv']
            card_expiry = form.cleaned_data['card_expiry']
            amount = form.cleaned_data['amount']

            try:
                customer = Customer.objects.get(email=request.user.email)
                customer.wallet += amount
                customer.save()
                return Response({'message': 'Wallet recharge successful'}, status=status.HTTP_200_OK)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST)



