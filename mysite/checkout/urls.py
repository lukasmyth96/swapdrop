from django.urls import path
from .views import checkout, shipping_address_redirect, pick_collection_time

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('shipping_address/', shipping_address_redirect, name='shipping-address-redirect'),
    path('pick_collection_time/', pick_collection_time, name='pick-collection-time')
]
