from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate,  update_session_auth_hash
from concert.models import Concert
from ticketkartapp.models import User
import datetime
from .forms import CustomUserCreationForm, PwdUpdateForm, UserForm


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
            return redirect('home')

    return render(request, 'update.html', {'form': form})


@login_required(login_url='login')
def updateUserPwd(request):
    form = PwdUpdateForm(user=request.user)
    if request.method == 'POST':
        form = PwdUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('home')
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