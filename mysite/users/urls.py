from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/info/', views.profile_info, name='profile-info')
    ]
