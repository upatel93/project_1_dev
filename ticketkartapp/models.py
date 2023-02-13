from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=12, null=True, unique=True)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    avatar = models.ImageField(null=True, default="avatar.svg")
    is_retailer = models.BooleanField(default=False)

    def __str__(self):
        user_type = "Normal User"
        if self.is_retailer:
            user_type = "Retailer"
        return f'{self.name} - {self.email} - {user_type}' 

    def deduct_balance(self, amount):
        if self.balance >= Decimal(amount):
            self.balance -= Decimal(amount)
            self.save()
            return True
        else:
            return False


class PaymentMethod(models.Model):
    PAYMENT_TYPES = [
        ('CC', 'Credit Card'),
        ('DC', 'Debit Card'),
        ('INT', 'Interac'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(choices=PAYMENT_TYPES, max_length=3)
    card_number = models.CharField(max_length=16, null=True)
    expiry_date = models.DateField(null=True)
    cvv = models.CharField(max_length=3, null=True)
    bank_name = models.CharField(max_length=100, null=True)
    account_number = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.name} - {self.get_payment_type_display()}'
    
    def verify(self):
        if self.payment_type == 'CC' or self.payment_type == 'DC':
            # credit/debit card verification here
            # check card number and expiry date against a database
            self.verified = True
            self.save()
            return True
        elif self.payment_type == 'INT':
            # Interac verification here
            # check bank name and account number against a database
            self.verified = True
            self.save()
            return True
        else:
            return False

    def make_payment(self, amount):
        if self.verified:
            # fake payment here
            # send a request to a fake payment gateway and return success or failure
            return True
        else:
            return False
