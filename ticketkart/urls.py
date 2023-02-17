"""ticketkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cart.views import add_to_cart, cart_detail, remove_item, update_item, checkout,order_detail
from .views import home, RegisterCustomer, user_logout, loginPage, updateUser, updateUserPwd, add_payment_method, add_balance, user_profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('',home,name="home"),
    path('add-to-cart/<int:concert_id>',add_to_cart, name="add-to-cart"),
    path('cart-detail/',cart_detail, name="cart-detail"),
    path('order_detail/<int:order_id>',order_detail,name="order-detail"),
    path('remove-item/<int:item_id>',remove_item, name="remove-item"),
    path('update-item/<int:item_id>',update_item, name="update-item"),
    path('checkout/',checkout, name='checkout' ),
    path('register/',RegisterCustomer, name="register"),
    path('logout/',user_logout, name='logout'),
    path('login/',loginPage,name="login"),
    path('update-user/',updateUser,name='update-user'),
    path('change-password/',updateUserPwd, name='change-password'),
    path('add-payment-method/', add_payment_method,name="add-payment-method"),
    path('add-balance/',add_balance,name="add-balance"),
    path('profile',user_profile,name="user-profile")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
