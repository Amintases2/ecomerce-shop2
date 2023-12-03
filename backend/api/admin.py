from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'balance',
                    'amount_of_deals', 'photo', 'is_staff', 'created_at')
    list_editable = ('balance', 'amount_of_deals')
    list_filter = ('id',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'discount', 'product_status_id', 'created_at', 'updated_at')
    list_editable = ('product_status_id',)


@admin.register(ProductSatus)
class ProductSatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(OrderStatus)
class OrderSatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'price', 'product_id', 'order_status', 'created_at')


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'global_discount', 'date_add_limit')
