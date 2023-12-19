from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone', 'birth_date', 'wallet']

    def create(self, validated_data):
        user_model = get_user_model()
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password'],
        }
        user = user_model.objects.create(**user_data)
        user.set_password(validated_data['password'])
        user.save()

        validated_data.pop('password', None)
        validated_data['user'] = user
        customer = Customer.objects.create(**validated_data)

        return customer

class WalletRechargeSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    card_cvv = serializers.CharField(max_length=4)
    card_expiry = serializers.CharField(max_length=5)
    amount = serializers.DecimalField(min_value=0.01, max_digits=10, decimal_places=2)

