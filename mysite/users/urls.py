from django.urls import path

from users.views import register, profile_info, ProfileProductsListView

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', ProfileProductsListView.as_view(), name='profile'),
    path('profile/info/', profile_info, name='profile-info')
    ]
