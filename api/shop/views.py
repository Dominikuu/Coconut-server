import json
from django.shortcuts import render, get_object_or_404
from django.http import  JsonResponse
from rest_framework import status
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from cart.forms import CartAddProductForm
from rest_framework.decorators import api_view
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all().values()
    products = Product.objects.filter(available=True).values()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug).values()
        products = products.filter(category=category).values()

    return JsonResponse({
        'text': 'test1',
        'category': category,
        'categories': list(categories),
        'products': list(products)
    })

@csrf_exempt
@api_view(['POST'])
def product_detail(request, product_id, slug):
    body = json.loads(request.body.decode('utf-8'))
    product_id = body.get('product_id')
    slug = body.get('slug')
    product = Product.objects.filter(id=product_id,
                                slug=slug,
                                available=True).values()
    return JsonResponse(
        {
            'product': list(product),
            'product_id': product_id,
            'slug': slug, 
        }
    )
