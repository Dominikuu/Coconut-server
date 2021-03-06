from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.decorators import action
from cart.models import Cart, CartItem

from .forms import OrderCreateForm
from .models import OrderItem
from .task import order_created

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart items to be viewed or edited.
    """
    queryset = OrderItem.objects.all()

    @action(detail=False,methods=['post'])
    def order_create(self,request):
        
        cart = Cart.objects.get(user=request.user)
        
        form = OrderCreateForm(request.data)
        print(form.is_valid())
        if form.is_valid():
            order = form.save()
            existing_cart_item = CartItem.objects.filter(cart=cart)
            # print(existing_cart_item, type(existing_cart_item))
            for item in existing_cart_item:
                print(item.product, type(item.product))
                OrderItem.objects.create(order=order,
                                            product=item.product,
                                            price=item.product.price,
                                            quantity=item.quantity)
            # clear the cart
            cart.delete()
            order_created(order.id)
            # request.session['order_id'] = order.id
            # redirect to the payment
            return redirect('payment:process')

        return Response({'message': 'success'}, status=status.HTTP_200_OK)
