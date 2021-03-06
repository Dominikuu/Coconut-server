from django.contrib.auth.models import User
from rest_framework import serializers
from shop.serializers import ProductSerializer
from .models import Cart, CartItem
 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source="product.name")
    slug = serializers.CharField(read_only=True, source="product.slug")
    image = serializers.CharField(read_only=True, source="product.image")
    price = serializers.DecimalField(read_only=True, source="product.price", max_digits=10, decimal_places=0)
 
    class Meta:
        model = CartItem
        fields = ('id', 'name', 'slug', 'quantity','price', 'image')

class CartSerializer(serializers.ModelSerializer):

    """Serializer for the Cart model."""

    user = UserSerializer(read_only=True)
    # used to represent the target of the relationship using its __unicode__ method
    items = CartItemSerializer(read_only=True, required=False, allow_null=True, default=None)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at','items']


