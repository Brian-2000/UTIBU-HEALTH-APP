# serializers.py

from rest_framework import serializers
from .models import User, Customer, Medication, Order, Statement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'admin', 'patient', 'name']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone_number', 'address']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'description', 'price', 'stock_quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'medication', 'user', 'quantity', 'order_date', 'is_delivered', 'pick_up_date', 'delivery_option']

class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ['id', 'customer', 'amount', 'date']
