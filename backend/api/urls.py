from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('auth/me', UserView.as_view()),
    path('products/', ProductsViewSet.as_view()),
    path('orders/', OrdersApiView.as_view()),
    path('adminproducts/', AdminProductsViewSet.as_view()),
    path('adminproducts/update/', AdminProduct.as_view()),
    path('adminusers/update/', AdminUser.as_view()),
    path('adminorders/', AdminOrdersViewSet.as_view()),
    path('adminorders/update/', UpdateAdminOrder.as_view()),
    path('users/', UsersViewSet.as_view()),
    path('settings/<int:pk>/', SettingsViewSet.as_view()),
    path('accounts/', include(("okta_oauth2.urls", "okta_oauth2"), namespace="okta_oauth2")),
]
