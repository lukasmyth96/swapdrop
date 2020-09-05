from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import start_checkout, shipping_address_redirect, pick_collection_time, confirm_payment

urlpatterns = [
    path('<int:product_id>/', login_required(start_checkout), name='checkout'),
    path('<int:product_id>/shipping_address/', login_required(shipping_address_redirect), name='shipping-address-redirect'),
    path('<int:product_id>/pick_collection_time/', login_required(pick_collection_time), name='pick-collection-time'),
    path('<int:product_id>/confirm_payment/time_slot=<int:selected_time_slot_id>', login_required(confirm_payment), name='confirm-payment')
]
