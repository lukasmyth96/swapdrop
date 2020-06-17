from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from dashboard.views import dashboard

urlpatterns = [
    path('', dashboard, name='dashboard')
]
