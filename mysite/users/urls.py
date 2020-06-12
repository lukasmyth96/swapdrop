from django.urls import path
from django.contrib.auth import views as auth_views

from users.views import register, profile_info, ProfileProductsListView, shipping_address_info
from users.forms import UserLoginForm

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', ProfileProductsListView.as_view(), name='profile'),
    path('profile/info/', profile_info, name='profile-info'),
    path('profile/address/', shipping_address_info, name='shipping-address-info')
    ]
