from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from users.views import register, Login, profile_info, ProfileYourItemsListView, ProfileOffersMadeListView, shipping_address_info
from users.forms import UserLoginForm

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', Login.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name=None), name='logout'),
    path('profile/your_items/', login_required(ProfileYourItemsListView.as_view()), name='profile-your-items'),
    path('profile/offers_made/', login_required(ProfileOffersMadeListView.as_view()), name='profile-offers-made'),
    path('profile/info/', login_required(profile_info), name='profile-info'),
    path('profile/address/', login_required(shipping_address_info), name='shipping-address-info')
    ]
