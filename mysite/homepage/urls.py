from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage-home'),
    path('land/', views.landing_page, name='landing-page')
    ]
