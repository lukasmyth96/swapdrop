from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from users.views import register, Login, profile_info, ProfileProductsListView, shipping_address_info
from users.forms import UserLoginForm

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', Login.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name=None), name='logout'),
    path('profile/', login_required(ProfileProductsListView.as_view()), name='profile'),
    path('profile/info/', login_required(profile_info), name='profile-info'),
    path('profile/address/', login_required(shipping_address_info), name='shipping-address-info')
    ]
