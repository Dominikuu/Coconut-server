import json
import jwt
from re import sub
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Product
from django.core import serializers
from .models import CartItem, Cart
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.decorators import action, list_route
from .serializers import CartSerializer,CartItemSerializer
from shop.models import Product

class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows carts to be viewed or edited.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request):
        try:
            cart =  Cart.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response({'message': 'Cart is not existed'}, status=status.HTTP_400_BAD_REQUEST)
        cartItem = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cartItem, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,methods=['post', 'put'])
    def add_to_cart(self, request):
        """Add an item to a user's cart.
        Adding to cart is disallowed if there is not enough inventory for the
        product available. If there is, the quantity is increased on an existing
        cart item or a new cart item is created with that quantity and added
        to the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.
        """
        cart =  Cart.objects.filter(user=request.user).first()
        if cart is None:
            cart = Cart(user=request.user)
            cart.save()

        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            return Response({'status': 'fail'})

        # Disallow adding to cart if available inventory is not enough
        if product.stock <= 0 or product.stock - quantity < 0:
            print ("There is no more product available")
            return Response({'status': 'fail'})

        existing_cart_item = CartItem.objects.filter(cart=cart,product=product).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = CartItem(cart=cart, product=product, quantity=quantity)
            new_cart_item.save()
        
        # return the updated cart to indicate success
        cartItem = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cartItem, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,methods=['post', 'put'])
    def remove_from_cart(self, request, pk=None):
        """Remove an item from a user's cart.
        Like on the Everlane website, customers can only remove items from the
        cart 1 at a time, so the quantity of the product to remove from the cart
        will always be 1. If the quantity of the product to remove from the cart
        is 1, delete the cart item. If the quantity is more than 1, decrease
        the quantity of the cart item, but leave it in the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.
        """
        cart =  Cart.objects.filter(user=request.user).first()
        if cart is None:
            cart = Cart(user=request.user)
            cart.save()

        try:
            product = Product.objects.get(
                pk=request.data['product_id']
            )
            
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})

        try:
            cart_item = CartItem.objects.get(cart=cart,product=product)
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})

        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        # if cart_item.quantity == 1:
        cart_item.delete()
        # else:
        #     cart_item.quantity -= 1
        #     cart_item.save()

        # return the updated cart to indicate success
        cartItem = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cartItem, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart items to be viewed or edited.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

def get_cart_count(request):
    cart = get_user_cart(request)
    total_count = 0
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        total_count += item.quantity
    return total_count


def update_cart_info(request):
    request.session['cart_count'] = get_cart_count(request)

@csrf_exempt
@require_POST
def cart_add(request, product_id):
    reqbody_unicode = request.body.decode('utf-8')
    reqbody = json.loads(reqbody_unicode)
    cart = get_user_cart(request)
    slug = reqbody.get('slug')
    quantity = reqbody.get('quantity')
    product = Product.objects.get(slug=slug)
  
    try:
        cartItem = CartItem.objects.get(cart=cart, product=product)
        cartItem.quantity = quantity
        cartItem.save()
    except ObjectDoesNotExist:
        cartItem = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        cartItem.save()


    if request.session.get('cart_count'):
        request.session['cart_count'] += quantity
    else:
        request.session['cart_count'] = quantity
    update_cart_info(request)
    print(serializers.serialize('json', [cartItem]))
    return HttpResponse(serializers.serialize('json', [cartItem]))
    # return JsonResponse(serializers.serialize('json', [cartItem]), safe=False)
    

@csrf_exempt
@require_POST
def cart_remove(request, product_id):
    cart_item = CartItem.objects.get(id=id)
    quantity = cart_item.quantity
    cart_item.delete()
    if request.session.get('cart_count'):
        request.session['cart_count'] -= quantity
    else:
        request.session['cart_count'] = 0
    update_cart_info(request)
    return JsonResponse({'cart': "category"})

# @login_required
def get_user_cart(request):
    """Retrieves the shopping cart for the current user."""
    cart = None
    print(request.user)

    try:
        cart = Cart.objects.get(user=request.user)
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart.save()
            
            # cart = Cart(user=request.user)
    # else:
    #     cart_id = request.session.get('cart_id')
    #     if not cart_id:
    #         cart = Cart()
    #         cart.save()
    #         request.session['cart_id'] = cart.id
    #     else:
    #         cart = Cart.objects.get(id=cart_id)
    return cart


def cart_detail(request):
    cart = get_user_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    order_total = Decimal(0.0)
    for item in cart_items:
        order_total += (item.product.price * item.quantity)
    return JsonResponse({'cart': cart, 'cart_items': cart_items, 'total': total})
