from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import CustomerManager
from django.conf import settings
from django.contrib.auth.models import User


UNIT_CHOICES = [
    ('cm', 'Centimeters'),
    ('mm', 'Millimeters'),
    ('piece', 'Piece'),
    ('pack', 'Pack'),
    ('box', 'Box'),
]

CATEGORY_CHOICES = [
    ('Тюльпаны', 'Тюльпаны'),
    ('Розы', 'Розы'),
    ('Лилии', 'Лилии'),
    ('Хризантемы', 'Хризантемы'),
    ('Незабудки', 'Незабудки'),
    ('Ромашки', 'Ромашки'),
    ('Георгины', 'Георгины'),
    ('Пионы', 'Пионы'),
    ('Орхидеи', 'Орхидеи'),
    ('Подсолнухи', 'Подсолнухи'),
    ('Ландыши', 'Ландыши'),
    ('Астры', 'Астры'),
    ('Сирень', 'Сирень'),
    ('Смешанные', 'Смешанные'),
]

COUNTRY_CHOICES = [
    ('Эквадор', 'Эквадор'),
    ('Колумбия', 'Колумбия'),
    ('Россия', 'Россия'),
    ('Узбекистан', 'Узбекистан'),
    ('Грузия', 'Грузия'),
    ('Россия', 'Россия'),
    ('Казахстан', 'Казахстан'),
    ('Эфиопия', 'Эфиопия'),
    ('Нидерланды', 'Нидерланды'),
    ('Кения', 'Кения'),
    ('Италия', 'Италия'),
    ('Беларусь', 'Беларусь'),
    ('Чили', 'Чили'),
    ('Испания', 'Испания'),
]

class Category(models.Model):
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Customer(AbstractUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    objects = CustomerManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customer_groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customer_user_permissions',
        help_text='Specific permissions for this user.',
    )

    def add_to_wallet(self, amount):
        self.wallet += amount
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Country (models.Model):
    name = models.CharField(max_length=20, choices=COUNTRY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products')
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    price = models.PositiveIntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class WalletTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.timestamp}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField('Product', through='OrderItem')
    total_price = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

