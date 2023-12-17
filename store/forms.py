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

class WalletTransactionForm(forms.ModelForm):
    class Meta:
        model = WalletTransaction
        fields = ['card_number', 'expiration_date', 'cvv', 'amount']

class PaymentForm(forms.Form):
    total = forms.IntegerField(widget=forms.HiddenInput())
    action = forms.CharField(widget=forms.HiddenInput())