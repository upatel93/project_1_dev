from django.contrib import admin
from .models import Cart, CartItem, Order,OrderItem

# Register your models here.

class CartInline(admin.TabularInline):
    model = CartItem 

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartInline
    ]
    list_display = ['customer', 'created_on', 'updated_on']


class OrderInline(admin.TabularInline):
    model = OrderItem 
    list_display = [
        "ticket",
        "quantity",
        "get_unit_price"
    ]

    def get_unit_price(self, obj):
        return obj.unit_price
    get_unit_price.short_description = 'Unit Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderInline
    ]
