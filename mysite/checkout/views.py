from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from users.forms import ShippingAddressUpdateForm
from products.models import Product
from products.model_enums import ProductStatus
from swaps.models import Swap
from swaps.models import SwapStatus


@login_required()
def checkout(request, product_id):
    """
    Entry-point for all checkouts - redirects to shipping-address-redirect if address not already given otherwise
    redirects to time-slot picker.
    """
    address_form = ShippingAddressUpdateForm(instance=request.user.profile)
    if address_form.is_initial_valid():
        # if shipping address already given redirect straight to time slot pick
        return redirect('pick-collection-time', product_id=product_id)
    else:
        return redirect('shipping-address-redirect', product_id=product_id)


@login_required()
def shipping_address_redirect(request, product_id):

    if request.method == 'POST':
        address_form = ShippingAddressUpdateForm(instance=request.user.profile, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return redirect('pick-collection-time', product_id=product_id)
    else:
        address_form = ShippingAddressUpdateForm(instance=request.user.profile)
        return render(request, 'checkout/shipping_address_redirect.html', context={'address_form': address_form})


@login_required()
def pick_collection_time(request, product_id):
    if request.method == 'POST':

        # Update status of product
        product = Product.objects.get(id=product_id)
        product.status = ProductStatus.CHECKOUT_COMPLETE
        product.save(update_fields=['status'])

        # Refresh status of Swap that product belongs to
        # TODO error handling if can't find or find more than one? shouldn't ever happen
        swap = Swap.objects.get((Q(offered_product=product) | Q(desired_product=product))
                                & Q(status=SwapStatus.PENDING_CHECKOUT))
        swap.refresh_status()  # internally updates status depending on status of the two products

        messages.success(request, 'Checkout complete')
        return redirect('profile')
    else:
        return render(request, template_name='checkout/pick_collection_time.html', context={'product_id': product_id})
