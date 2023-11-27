from django import forms
from .models import *

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'birth_date']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


