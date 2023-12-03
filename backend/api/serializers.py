from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'amount_of_deals', 'is_staff', 'balance',
                  'photo']


class ProductSerializer(serializers.ModelSerializer):
    product_status_title = serializers.CharField(source='product_status_id.title')
    product_status_id = serializers.CharField(source='product_status_id.pk')

    class Meta:
        model = Products
        fields = ['id', 'title', 'description', 'price', 'discount', 'photo',
                  'product_status_title', 'product_status_id']


class OrderSerializer(serializers.ModelSerializer):
    # user_id = serializers.CharField(source='user_id.pk')
    order_status_title = serializers.CharField(source='order_status.title')
    product_id_title = serializers.CharField(source='product_id.title')
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    user_id_title = serializers.CharField(source='user_id.username')

    class Meta:
        model = Orders
        fields = ['id', 'user_id', 'user_id_title', 'price', 'order_status', 'order_status_title', 'product_id',
                  'product_id_title',
                  'created_at']


class SettingsSerializer(serializers.ModelSerializer):
    date_add_limit = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Settings
        fields = ['id', 'global_discount', 'date_add_limit']
