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

class WalletRechargeForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    card_cvv = forms.CharField(label='Card CVV', max_length=4)
    card_expiry = forms.CharField(label='Card Expiry (MM/YY)', max_length=7)
    amount = forms.DecimalField(label='Amount', min_value=0.01)