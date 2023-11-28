from django.urls import path
from .views import *


urlpatterns = [
    path('', homeView, name='home_url'),
    path('sign_in', signInView, name='sign_in_url'),
    path('sign_up', signUpView, name='sign_up_url'),
    path('sign_out', signOutView, name='sign_out_url'),
    path('products', productsView, name='products_url'),
    path('product/<int:product_id>/', view_product, name='view_product_url'),
    path('update_product/<int:product_id>/', update_product, name='update_product_url'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product_url'),
    path('add_product', add_product, name='add_product_url'),
    path('add_to_cart/<int:product_id>', addToCartView, name='add_cart_url'),
    path('cart_detail', cartDetailView, name='cart_detail_url'),
    path('profile', profileView, name='profile_url'),
    path('products/<int:category_id>', productsByCategoryView, name='products_by_category_url'),
    path('profile/', profileView, name='profile_url'),
    path('profile/edit/', profileEditView, name='profile_edit_url'),
    path('profile/delete/', profileDeleteView, name='profile_delete_url'),
    path('remove_from_cart/<int:product_id>', removeProductFromCartView, name='remove_from_cart_url'),
]


