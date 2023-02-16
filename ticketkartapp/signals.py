from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

from cart.models import Cart

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
