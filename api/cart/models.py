from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from shop.models import Product

class Cart(models.Model):
    # user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User,
        related_name='user',
        on_delete=models.CASCADE
    )
    
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Cart #' + unicode(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='cartItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Order #' + unicode(self.id) + ' of ' + self.product.title