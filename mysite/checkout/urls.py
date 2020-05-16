from django.urls import path
from .views import shipping_address_redirect

urlpatterns = [
    path('shipping_address/', shipping_address_redirect.as_view(), name='shipping_address_redirect'),
]
