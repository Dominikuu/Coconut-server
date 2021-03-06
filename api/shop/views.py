from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
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
    # body_unicode = request.body.decode('utf-8')
    # body = json.loads(body_unicode)
    # product_id = body['product_id']
    # slug = body['slug']
    # product = get_object_or_404(Product,
    #                             id=product_id,
    #                             slug=slug,
    #                             available=True)
    product = Product.objects.filter(id=product_id,
                                slug=slug,available=True).values()
    return JsonResponse({'product': list(product),
                   'product_id': product_id, 'slug': slug})
