import uuid
from django.db.models import Sum, F
from django.db import models
from ticketkartapp.models import User
from concert.models import ConcertTicket

class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.customer.name}'s Cart"
    
    @property
    def cart_total(self):
        return self.cartitem_set.annotate(
            item_total=F('quantity') * F('ticket__price')
        ).aggregate(total=Sum('item_total'))['total']

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ticket = models.ForeignKey(ConcertTicket, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{str(self.ticket)}'



class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)

    @property
    def order_total(self):
        return self.orderitem_set.annotate(
            item_total=F('quantity') * F('ticket__price')
        ).aggregate(total=Sum('item_total'))['total']
    
    def __str__(self) -> str:
        return f"{self.customer.name}'s order Placed at {self.placed_at}"


class OrderItem(models.Model):
    uniq_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    ticket = models.ForeignKey(ConcertTicket, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

    @property
    def unit_price(self):
        return self.ticket.price
    
    def __str__(self):
        return f'{str(self.ticket.concert.name)} - {self.ticket.seat_type}- {self.quantity}'