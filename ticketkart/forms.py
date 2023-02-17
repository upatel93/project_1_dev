from django import forms
from django.forms import ModelForm, TextInput, TimeField, Select,EmailInput,PasswordInput,FileInput, HiddenInput,DateInput
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from ticketkartapp.models import User, PaymentMethod


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','name', 'email', 'phone', 'is_retailer', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'phone': 'Phone',
            'is_retailer': 'Are you a retailer?',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'avatar','first_name', 'last_name','phone']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'first_name':TextInput(attrs={'class': 'form-control'}),
            'last_name':TextInput(attrs={'class': 'form-control'}),
            'phone':TextInput(attrs={'class': 'form-control'}),
            'avatar':FileInput(attrs={'class': 'form-control'}),
        }

class PwdUpdateForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password1', 'password2','old_password']
        widgets = {
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
            'old_password': PasswordInput(attrs={'class': 'form-control'}),
        }


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['payment_type', 'card_number', 'expiry_date', 'cvv']
        widgets = {
            'expiry_date':DateInput(attrs={'class': 'form-control'}),
        }

class BalanceForm(forms.Form):
    amount = forms.DecimalField(max_digits=6, decimal_places=2)