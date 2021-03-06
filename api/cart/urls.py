# from django.conf.urls import url

# from . import views

# urlpatterns = [
#     url(r'^$', views.cart_detail,
#         name='cart_detail'),
#     url(r'^add/(?P<product_id>\d+)/$',
#         views.cart_add,
#         name='cart_add'),
#     url(r'^remove/(?P<product_id>\d+)/$',
#         views.cart_remove,
#         name='cart_remove'),
# ]
from django.urls import path,include
from rest_framework import routers

from .views import (CartViewSet,CartItemViewSet)

app_name = 'cart'

router = routers.DefaultRouter()
router.register(r'', CartViewSet)
router.register(r'cart_items',CartItemViewSet)

urlpatterns = [
    path('',include(router.urls))
]