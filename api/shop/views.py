from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all().values()
    products = Product.objects.filter(available=True).values()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug).values()
        products = products.filter(category=category).values()

    return JsonResponse({'category': category,
                   'categories': list(categories),
                   'products': list(products)})


def product_detail(request, product_id, slug):
    product = get_object_or_404(Product,
                                id=product_id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
