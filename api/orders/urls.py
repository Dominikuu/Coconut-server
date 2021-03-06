from django.urls import path,include
from rest_framework import routers
from .views import OrderViewSet

app_name = 'orders'

router = routers.DefaultRouter()
router.register(r'', OrderViewSet)

urlpatterns = [
    path('',include(router.urls))
]