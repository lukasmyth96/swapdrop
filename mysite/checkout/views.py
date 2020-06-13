import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from users.forms import ShippingAddressUpdateForm
from products.models import Product
from products.model_enums import ProductStatus
from swaps.models import Swap
from swaps.models import SwapStatus
from bookings.models import TimeSlot, Booking
from bookings.model_enums import BookingType
from checkout.permissions import owns_product, verify_checkout_progress, CheckoutStatus


@owns_product
def start_checkout(request, product_id):
    """
    Entry-point for all checkouts - redirects to shipping-address-redirect if address not already given otherwise
    redirects to time-slot picker.
    """
    if request.method == 'POST':
        address_form = ShippingAddressUpdateForm(instance=request.user.profile)

        request.session['checkout_status'] = {product_id: CheckoutStatus.CHECKOUT_STARTED.name}

        if address_form.is_initial_valid():
            # if shipping address already given redirect straight to time slot pick
            request.session['checkout_status'] = {product_id: CheckoutStatus.ADDRESS_GIVEN.name}
            return redirect('pick-collection-time', product_id=product_id)
        else:
            return redirect('shipping-address-redirect', product_id=product_id)
    else:
        users_product = Product.objects.get(id=product_id)
        try:
            swap = Swap.objects.get((Q(offered_product=users_product) | Q(desired_product=users_product)) & Q(status=SwapStatus.PENDING_CHECKOUT))
            incoming_product = swap.desired_product if users_product == swap.offered_product else swap.offered_product
            context = {'users_product': users_product, 'incoming_product': incoming_product}
            return render(request, template_name='checkout/checkout.html', context=context)
        except Swap.DoesNotExist:
            messages.warning(request, 'oops.. looks like this product isn\'t ready for checkout yet')
            return redirect('profile')


@verify_checkout_progress(required_checkout_status=CheckoutStatus.CHECKOUT_STARTED)
@owns_product
def shipping_address_redirect(request, product_id):

    if request.method == 'POST':
        address_form = ShippingAddressUpdateForm(instance=request.user.profile, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            request.session['checkout_status'] = {product_id: CheckoutStatus.ADDRESS_GIVEN.name}
            return redirect('pick-collection-time', product_id=product_id)
    else:
        address_form = ShippingAddressUpdateForm(instance=request.user.profile)
        return render(request, 'checkout/shipping_address_redirect.html', context={'address_form': address_form})


@verify_checkout_progress(required_checkout_status=CheckoutStatus.ADDRESS_GIVEN)
@owns_product
def pick_collection_time(request, product_id):

    if request.method == 'POST':
        try:
            selected_time_slot_id = int(request.POST.get('time-slot-radio'))
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
        max_date_to_show = datetime.date.today() + datetime.timedelta(days=5)
        time_slots = TimeSlot.objects.filter(date__lte=max_date_to_show)  # get all slots within next n days
        time_slots = [slot for slot in time_slots if slot.is_available]
        grouped_time_slots = _group_time_slots(time_slots)
        context = {'product_id': product_id,
                   'grouped_time_slots': grouped_time_slots}
        return render(request, template_name='checkout/pick_collection_time.html', context=context)


def _group_time_slots(time_slots):
    """
    Groups list of TimeSlot objects into a list[list[TimeSLot]] where each sublist contains the timeslots for a single
    day.
    Parameters
    ----------
    time_slots: list[TimeSLot]

    Returns
    -------
    grouped_time_slots: list[list[TimeSlot]]
    """

    def date_range(start_date, end_date):
        """ Iterator - yields all dates in range (inclusive)"""
        for n in range(int((end_date - start_date).days)+1):
            yield start_date + datetime.timedelta(n)

    grouped_time_slots = []
    if time_slots:
        max_date = max([ts.date for ts in time_slots])  # get max date among time slots
        for date in date_range(datetime.date.today(), max_date):
            grouped_time_slots.append([ts for ts in time_slots if ts.date == date])

    return grouped_time_slots


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



