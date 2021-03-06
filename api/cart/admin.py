from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at',
                    'updated_at']
    list_filter = ['created_at', 'user', 'updated_at']
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)
