from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing-page'),
    path('terms/', views.terms_of_service, name='terms-of-service'),
    ]
