"""django_rest_framework_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from user import views as userViews
from django.http import HttpResponse
from rest_framework_jwt.views import (obtain_jwt_token,
                                        verify_jwt_token,
                                        refresh_jwt_token)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth', obtain_jwt_token),
    url(r'^api-token-refresh', refresh_jwt_token),
    url(r'^api-token-verify', verify_jwt_token),
    url(r'^api-register-user', userViews.CreateUserView.as_view()),
    url(r'^api-login-user', userViews.LoginUserView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^payment/', include('payment.urls', namespace='payment')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^product/', include('shop.urls', namespace='shop')),

]
