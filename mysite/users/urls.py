from django.urls import path

from users.views import register, profile_info, ProfileProductsListView, shipping_address_info

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', ProfileProductsListView.as_view(), name='profile'),
    path('profile/info/', profile_info, name='profile-info'),
    path('profile/address/', shipping_address_info, name='shipping-address-info')
    ]
