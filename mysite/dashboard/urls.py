from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import views as auth_views

from dashboard.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard')
]
