from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate,  update_session_auth_hash
from concert.models import Concert, ConcertTicket
from cart.models import Cart, CartItem,Order, OrderItem
from ticketkartapp.models import User, PaymentMethod
import datetime
from .forms import CustomUserCreationForm, PwdUpdateForm, UserForm, PaymentMethodForm, BalanceForm
from decimal import Decimal


def home(request):
    today_date=datetime.date.today()
    if request.method == "GET":
        queryset = Concert.objects.filter(date__gte=today_date).order_by("date")
        context = {
            "concerts" : list(queryset)
        }
        return render(request,'home.html',context)
    if request.method == "POST":
        q_name = request.POST.get('concert')
        q_date = request.POST.get('date')
        q_location = request.POST.get('location')
        q_name = q_name.lower()
        q_date = q_date if len(q_date) > 0 else today_date
        queryset_1 = Concert.objects.select_related('venue').filter(Q(date__gte=q_date),Q(name__icontains=q_name),Q(venue__location__icontains=q_location)).order_by("date")
        context_2 = {
        "concerts" : list(queryset_1)
        }
        return render(request, 'home.html', context_2)


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('home')

def RegisterCustomer(request):
    if request.user.is_authenticated:
        return redirect('logout')
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'register.html', {'form': form})



@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        print(request.FILES)
        if form.is_valid():
            form.save()
            # print(form.errors)
            return redirect('user-profile')

    return render(request, 'update.html', {'form': form})


@login_required(login_url='login')
def updateUserPwd(request):
    form = PwdUpdateForm(user=request.user)
    if request.method == 'POST':
        form = PwdUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('user-profile')
    else:
        form = PwdUpdateForm(request.user)
    return render(request, 'updatepwd.html', {'form': form})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        username = username.lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'login.html')

@login_required(login_url='login')
def add_payment_method(request):

    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = request.user
            payment_method.save()
            return redirect('add-balance')
    else:
        form = PaymentMethodForm()

    return render(request, 'add_payment_method.html', {'form': form})




@login_required(login_url='login')
def add_balance(request):
    payment_methods = PaymentMethod.objects.filter(user=request.user)

    if not payment_methods:
        return redirect('add-payment-method')

    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            payment_method_id = request.POST.get('payment_method')
            payment_method = PaymentMethod.objects.get(id=payment_method_id)

            if not payment_method.verified:
                payment_method.verify()
                if not payment_method.verified:
                    return redirect('add_balance')

            if payment_method.make_payment(amount):
                request.user.balance += Decimal(amount)
                request.user.save()
                return redirect('user_profile')
    else:
        form = BalanceForm()

    return render(request, 'add_balance.html', {'form': form, 'payment_methods': payment_methods})


@login_required(login_url='login')
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(customer=user)[:5]
    payment_methods = PaymentMethod.objects.filter(user=user)

    context = {
        "user" : user,
        "orders" : orders,
        "payment_methods": payment_methods
    }

    return render(request, "profile.html",context)

