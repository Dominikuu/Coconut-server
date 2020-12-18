from  rest_framework import serializers
from  .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            first_name,
            last_name,
            email,
            address,
            postal_code,
            city,
            created,
            updated,
            paid
        )

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            order,
            product,
            price,
            quantity
        ) 