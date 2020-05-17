import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from users.forms import ShippingAddressUpdateForm
from products.models import Product
from products.model_enums import ProductStatus
from swaps.models import Swap
from swaps.models import SwapStatus
from bookings.models import TimeSlot, Booking
from bookings.model_enums import BookingType


@login_required()
def start_checkout(request, product_id):
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
        try:
            selected_time_slot_id = int(request.POST['time-slot-select'])
        except ValueError:
            messages.warning(request, 'select an available time slot')
            return redirect('pick-collection-time', product_id=product_id)  # try again

        # Create collection booking within selected time-slot
        selected_time_slot = TimeSlot.objects.get(id=selected_time_slot_id)
        _create_booking(selected_time_slot=selected_time_slot, product_id=product_id, owner=request.user)
        time_slot_str = selected_time_slot.date.strftime('%A') + ' at ' + selected_time_slot.time.label
        messages.success(request, f'Collection booking confirmed for {time_slot_str}')

        # TODO in future this will move to after payment
        # Complete Checkout - updates status of Product and Swap
        checkout_successful = _complete_checkout(product_id)  # TODO what if checkout completion fails?
        if checkout_successful:
            messages.success(request, 'Checkout completed successfully')
        else:
            messages.error(request, 'Error occurred during checkout completion')

        return redirect('profile')

    else:  # GET request
        time_slots = TimeSlot.objects.all()  # FIXME starting with all for simplicity
        time_slots = [slot for slot in time_slots if slot.is_available]
        context = {'product_id': product_id,
                   'time_slots': time_slots}
        return render(request, template_name='checkout/pick_collection_time.html', context=context)


def _create_booking(selected_time_slot, product_id, owner):
    """ Create and save collection Booking in chosen time slot"""
    product = Product.objects.get(id=product_id)
    booking = Booking(time_slot=selected_time_slot,
                      owner=owner,
                      product=product,
                      booking_type=BookingType.COLLECTION)
    booking.save()



def _complete_checkout(product_id):
    """
    Function to be called upon successful checkout. Updates status of product and Swap.

    Returns
    -------
    success: bool
        True if updated succesfully
    """

    # Update status of product
    try:
        product = Product.objects.get(id=product_id)
        product.status = ProductStatus.CHECKOUT_COMPLETE
        product.save(update_fields=['status'])

        # Refresh status of Swap that product belongs to
        # TODO error handling if can't find or find more than one? shouldn't ever happen
        swap = Swap.objects.get((Q(offered_product=product) | Q(desired_product=product))
                                & Q(status=SwapStatus.PENDING_CHECKOUT))
        swap.refresh_status()  # internally updates status depending on status of the two products
        return True
    except:
        return False



