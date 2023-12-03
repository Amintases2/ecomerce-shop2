from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


def user_directory_path(instance, filename):
    return "user-photo/{0}/{1}".format(instance.user.id, filename)


class User(AbstractUser):
    balance = models.FloatField(default=0)
    photo = models.ImageField(blank=True, default='uploads/user-photo/default.jpg',
                              upload_to=f"uploads/{user_directory_path}")
    amount_of_deals = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class ProductSatus(models.Model):
    class Meta:
        verbose_name = 'Product status'
        verbose_name_plural = 'Product Statuses'

    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Products(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    title = models.CharField(max_length=64)
    description = models.TextField()
    photo = models.ImageField(upload_to=f"uploads/products/")
    product_status_id = models.ForeignKey(ProductSatus, null=True, blank=True, on_delete=models.SET_NULL,
                                          default=ProductSatus.objects.get(title='Active').id)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OrderStatus(models.Model):
    class Meta:
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Statuses'

    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Orders(models.Model):
    product_id = models.ForeignKey(Products, null=True, blank=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    order_status = models.ForeignKey(OrderStatus, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Settings(models.Model):
    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'

    global_discount = models.FloatField(default=0)
    date_add_limit = models.DateTimeField()
