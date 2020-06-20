from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import start_checkout, shipping_address_redirect, pick_collection_time

urlpatterns = [
    path('<int:product_id>/', login_required(start_checkout), name='checkout'),
    path('<int:product_id>/shipping_address/', login_required(shipping_address_redirect), name='shipping-address-redirect'),
    path('<int:product_id>/pick_collection_time/', login_required(pick_collection_time), name='pick-collection-time')
]
