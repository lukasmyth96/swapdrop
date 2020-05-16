from django.urls import path
from .views import checkout, shipping_address_redirect, pick_collection_time

urlpatterns = [
    path('<int:product_id>/', checkout, name='checkout'),
    path('<int:product_id>/shipping_address/', shipping_address_redirect, name='shipping-address-redirect'),
    path('<int:product_id>/pick_collection_time/', pick_collection_time, name='pick-collection-time')
]
