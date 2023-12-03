import time
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView

from .serializers import *


class CustomAuth(GenericAPIView):

    def post(self, request, *args, **kwargs):
        query_params = {'client_id': settings.OKTA_AUTH["CLIENT_ID"],
                        'redirect_uri': settings.OKTA_AUTH["REDIRECT_URI"],
                        'scope': "openid email profile",
                        'state': session['app_state'],
                        'code_challenge': code_challenge,
                        'code_challenge_method': 'S256',
                        'response_type': 'code',
                        'response_mode': 'query'}

        # build request_uri
        request_uri = "{base_url}?{query_params}".format(
            base_url=config["auth_uri"],
            query_params=requests.compat.urlencode(query_params)
        )


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pages', {'page_now': self.page.number,
                       'page_next': self.get_next_page(),
                       'page_previous': self.get_previous_page(),
                       'end_page': self.page.paginator.num_pages}),
            ('results', data)
        ]))

    def get_next_page(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_page(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()


class OrdersApiView(ListModelMixin, CreateModelMixin,
                    GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Orders.objects.filter(user_id=self.request.user).order_by('order_status')

    def get(self, request, *args, **kwargs):
        time.sleep(0.5)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(self.request.user.amount_of_deals)
        if Products.objects.filter(pk=self.request.data['product_id']).exists() and \
                OrderStatus.objects.filter(pk=self.request.data['order_status']).exists() and \
                self.request.user.amount_of_deals > 0:

            product = Products.objects.get(pk=request.data['product_id'])
            if product.product_status_id == ProductSatus.objects.get(title='Active'):
                order_status = OrderStatus.objects.get(pk=request.data['order_status'])
                final_price = product.price * (1 - product.discount / 100)

                order = Orders(
                    user_id=self.request.user,
                    product_id=product,
                    order_status=order_status,
                    price=final_price
                )
                order.save()

                product.product_status_id = ProductSatus.objects.get(title='Booked')
                product.save()

                self.request.user.amount_of_deals -= 1
                self.request.user.save()

                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(self.request.user)
        return JsonResponse(serializer.data)


class UsersViewSet(ListModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        title_like = self.request.GET.get('title')
        if title_like:
            return User.objects.filter(username__icontains=title_like)
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        time.sleep(0.5)
        return self.list(request, *args, **kwargs)


class ProductsViewSet(ListModelMixin, GenericAPIView):
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        title_like = self.request.GET.get('title')

        if title_like:
            return Products.objects.filter(product_status_id=1, title__icontains=title_like).order_by('-created_at')
        return Products.objects.filter(product_status_id=1).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        time.sleep(0.5)
        return self.list(request, *args, **kwargs)


class AdminProductsViewSet(ListModelMixin, GenericAPIView):
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAdminUser,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        title_like = self.request.GET.get('title')
        if title_like:
            return Products.objects.filter(product_status_id=1, title__icontains=title_like).order_by('-created_at')
        return Products.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        time.sleep(0.5)
        return self.list(request, *args, **kwargs)


class AdminProduct(GenericAPIView):
    # parser_classes = (FileUploadParser,)
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        data = self.request.data
        product = Products.objects.get(id=data.get('id'))
        product.title = data.get('title')
        product.description = data.get('description')
        product.price = data.get('price')
        product.discount = data.get('discount')
        product.save()

        return Response(HTTP_202_ACCEPTED)


class SettingsViewSet(UpdateModelMixin, RetrieveModelMixin, GenericAPIView):
    serializer_class = SettingsSerializer
    permission_classes = (IsAdminUser,)
    queryset = Settings.objects.filter(id=1)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        global_discount = self.request.data.get('global_discount')
        if global_discount:
            Products.objects.all().update(discount=global_discount)
        return self.update(request, *args, **kwargs)


class AdminOrdersViewSet(ListModelMixin, GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        title = self.request.GET.get('title')
        if self.request.GET.get('title'):
            return Orders.objects.filter(Q(id__icontains=title) | Q(user_id__username__icontains=title))
        return Orders.objects.all()

    def get(self, requests, *args, **kwargs):
        return self.list(requests, *args, **kwargs)

    def post(self, requests, *args, **kwargs):
        orders = self.get_queryset()

        cons = orders.filter(order_status_id=1).count()
        booked = orders.filter(order_status_id=2).count()
        sold = orders.filter(order_status_id=3).count()
        canceled = orders.filter(order_status_id=4).count()
        all_orders = orders.count()

        return JsonResponse({
            'cons': cons,
            'booked': booked,
            'sold': sold,
            'canceled': canceled,
            'all': all_orders
        })


class UpdateAdminOrder(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = OrderSerializer

    def put(self, requests, *args, **kwargs):
        print(self.request.data)
        id = self.request.data.get('id')
        order_status = self.request.data.get('order_status')

        order = Orders.objects.get(id=id)
        order.order_status = OrderStatus.objects.get(id=order_status)
        order.save()

        if order_status == '4':
            order.user_id.amount_of_deals += 1
            order.user_id.save()
            order.product_id.product_status_id = ProductSatus.objects.get(id=1)
            order.product_id.save()

        return Response(HTTP_202_ACCEPTED)


class AdminUser(GenericAPIView):
    permission_classes = (IsAdminUser,)

    def put(self, requests, *args, **kwargs):
        id = self.request.data.get('id')
        user = User.objects.get(id=id)
        user.amount_of_deals = self.request.data.get('amount_of_deals')
        user.save()
        return Response(HTTP_202_ACCEPTED)
