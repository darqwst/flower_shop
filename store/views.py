from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import *
from .forms import *


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


def signInView(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all()
        }
        return render(request=request, template_name='sign_in.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_url')
        context = {
            'error': 'Не верный логин и/или пароль',
            'email': email,
            'categories': Category.objects.all()
        }
        return render(request=request, template_name='sign_in.html', context=context)


def signUpView(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all()
        }
        return render(request=request, template_name='sign_up.html', context=context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        birth_date = request.POST.get('birth_date')
        try:
            Customer.object.get(email=email)
        except Customer.DoesNotExist:
            customer = Customer(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                birth_date=birth_date
            )
            customer.set_password(password)
            customer.save()
            return redirect('sign_in_url')
        else:
            context = {
                'error': 'This email is already taken!',
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'birth_date': birth_date,
                'categories': Category.objects.all()
            }
            return render(request=request, template_name='sign_up.html', context=context)


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