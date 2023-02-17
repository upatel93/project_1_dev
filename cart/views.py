from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from concert.models import Concert,ConcertTicket
from cart.models import Cart, CartItem, Order, OrderItem
from .forms import CartItemForm
from decimal import Decimal



@login_required(login_url='login')
def add_to_cart(request, concert_id):
    user = request.user
    cart = user.cart
    concert = Concert.objects.select_related('venue').get(id=concert_id)
    tickets = ConcertTicket.objects.filter(concert=concert_id)
    if request.method == "GET":
        context = {
            "user" : user,
            "cart" : cart,
            "concert" : concert,
            "tickets" : tickets,
        }
        return render(request,'addtocarttemp.html',context)
    if request.method == "POST":
        for ticket in tickets:
            if int(request.POST.get(str(ticket.id))) > 0:
                checkitem = CartItem.objects.filter(cart=cart, ticket=ticket).first()
                if checkitem:
                    # If the item exists, increase the quantity
                    new_qty = checkitem.quantity + int(request.POST.get(str(ticket.id)))
                    saving = CartItem.objects.filter(id=checkitem.id).update(quantity=new_qty)
                else:
                    CartItem.objects.create(cart=cart,ticket=ticket,quantity=int(request.POST.get(str(ticket.id))))
        return redirect("cart-detail")

@login_required(login_url='login')
def cart_detail(request):
    user = request.user
    cart = user.cart
    cartItems = CartItem.objects.select_related('ticket').filter(cart=cart)

    context = {
        "user" : user,
        "cart" : cart,
        "items" : cartItems
    }

    return render(request, "cartdetail.html",context)
    
@login_required(login_url='login')
def order_detail(request,order_id):
    user = request.user
    order = Order.objects.get(pk=order_id)
    orderItems = OrderItem.objects.select_related('ticket').filter(order=order)

    context = {
        "user" : user,
        "order" : order,
        "items" : orderItems
    }

    return render(request, "orderdetail.html",context)


@login_required(login_url='login')
def remove_item(request,item_id):
    item = CartItem.objects.get(pk=item_id)

    if request.method == "GET":
        return render(request,"removeitem.html",{"item":item})
    if request.method == "POST":
        item.delete()
        return redirect("cart-detail")
    
@login_required(login_url='login')
def update_item(request,item_id):
    item = CartItem.objects.get(pk=item_id)

    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('cart-detail')
    else:
        form = CartItemForm(instance=item)
    return render(request, 'edit_cart_item.html', {'form': form, "item":item})

@login_required(login_url='login')
def checkout(request):
    user = request.user
    cart = user.cart
    cart_items = cart.cartitem_set.all()
    errors = list()
    #  chacking to user balance
    if (user.balance+1) < cart.cart_total:
         errors.append(f"Your Banalce is {user.balance}, However, Cart's Total is {round(cart.cart_total,2)}. Please go to your profile and add required balance.")
        
    # checking for seats availability
    for item in cart_items:
         left = item.ticket.seats_left()
         if left < item.quantity:
             errors.append(f"{item.ticket} is sold out. It has seats {left} left")

    if errors:
        cartItems = CartItem.objects.select_related('ticket').filter(cart=cart)
        context = {
            "user" : user,
            "cart" : cart,
            "items" : cartItems,
            "errors" : errors,
        }
        return render(request, "cartdetail.html",context)
    else:
        order = Order.objects.create(customer=request.user)
        order_items = list()
        for item in cart.cartitem_set.all():
            order_item = OrderItem.objects.create(order=order, ticket=item.ticket, quantity=item.quantity)
            order_items.append(order_item)
        
        for cart_item in cart_items:
            cart_item.ticket.concert.increase_sold_seats(cart_item.quantity)
        
        user.deduct_balance(cart.cart_total)

        cart.cartitem_set.all().delete()

        context =  {
            "user" : user,
            "order" : order,
        }
        return render(request,'success.html',context)