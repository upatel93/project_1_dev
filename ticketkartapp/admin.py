from django.contrib import admin
from .models import User, PaymentMethod
# Register your models here.


class PaymentMethodInline(admin.StackedInline):
    model = PaymentMethod
    max_num = 3



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        PaymentMethodInline
    ]
    list_display = ['name', 'email', 'balance', 'is_retailer']


