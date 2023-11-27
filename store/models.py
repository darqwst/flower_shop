from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from .managers import CustomerManager


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
    ('Пионы', 'Пионы'),
    ('Астры', 'Астры'),
    ('Сирень', 'Сирень'),
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


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    wallet = models.PositiveIntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customer_user_permissions',
        help_text='Specific permissions for this user.',
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customer_groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = CustomerManager()

    def __str__(self):
        return self.email

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