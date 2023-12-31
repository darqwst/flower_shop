# Generated by Django 5.0 on 2023-12-19 12:32

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Тюльпаны', 'Тюльпаны'), ('Розы', 'Розы'), ('Лилии', 'Лилии'), ('Хризантемы', 'Хризантемы'), ('Незабудки', 'Незабудки'), ('Ромашки', 'Ромашки'), ('Георгины', 'Георгины'), ('Пионы', 'Пионы'), ('Орхидеи', 'Орхидеи'), ('Подсолнухи', 'Подсолнухи'), ('Ландыши', 'Ландыши'), ('Астры', 'Астры'), ('Сирень', 'Сирень'), ('Смешанные', 'Смешанные')], max_length=20)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Эквадор', 'Эквадор'), ('Колумбия', 'Колумбия'), ('Россия', 'Россия'), ('Узбекистан', 'Узбекистан'), ('Грузия', 'Грузия'), ('Россия', 'Россия'), ('Казахстан', 'Казахстан'), ('Эфиопия', 'Эфиопия'), ('Нидерланды', 'Нидерланды'), ('Кения', 'Кения'), ('Италия', 'Италия'), ('Беларусь', 'Беларусь'), ('Чили', 'Чили'), ('Испания', 'Испания')], max_length=20)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='products')),
                ('country', models.CharField(choices=[('Эквадор', 'Эквадор'), ('Колумбия', 'Колумбия'), ('Россия', 'Россия'), ('Узбекистан', 'Узбекистан'), ('Грузия', 'Грузия'), ('Россия', 'Россия'), ('Казахстан', 'Казахстан'), ('Эфиопия', 'Эфиопия'), ('Нидерланды', 'Нидерланды'), ('Кения', 'Кения'), ('Италия', 'Италия'), ('Беларусь', 'Беларусь'), ('Чили', 'Чили'), ('Испания', 'Испания')], max_length=20)),
                ('price', models.PositiveIntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unit', models.CharField(choices=[('cm', 'Centimeters'), ('mm', 'Millimeters'), ('piece', 'Piece'), ('pack', 'Pack'), ('box', 'Box')], max_length=20)),
                ('category', models.CharField(choices=[('Тюльпаны', 'Тюльпаны'), ('Розы', 'Розы'), ('Лилии', 'Лилии'), ('Хризантемы', 'Хризантемы'), ('Незабудки', 'Незабудки'), ('Ромашки', 'Ромашки'), ('Георгины', 'Георгины'), ('Пионы', 'Пионы'), ('Орхидеи', 'Орхидеи'), ('Подсолнухи', 'Подсолнухи'), ('Ландыши', 'Ландыши'), ('Астры', 'Астры'), ('Сирень', 'Сирень'), ('Смешанные', 'Смешанные')], max_length=20)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('wallet', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customer_groups', to='auth.group', verbose_name='groups')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customer_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.PositiveIntegerField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='store.OrderItem', to='store.product'),
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16)),
                ('expiration_date', models.CharField(max_length=5)),
                ('cvv', models.CharField(max_length=4)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
