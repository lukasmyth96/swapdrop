import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from users.forms import ShippingAddressUpdateForm
from products.models import Product
from products.model_enums import ProductStatus
from swaps.models import Swap
from swaps.models import SwapStatus
from bookings.models import TimeSlot
from checkout.permission_decorators import owns_product
from checkout.view_funcs import user_has_valid_address, create_collection_booking, group_time_slots_by_day


@owns_product
def start_checkout(request, product_id):
    """
    Entry-point for all checkouts - redirects to shipping-address-redirect if address not already given otherwise
    redirects to time-slot picker.
    """
    if request.method == 'POST':

        if user_has_valid_address(user=request.user):
            return redirect('pick-collection-time', product_id=product_id)
        else:
            return redirect('shipping-address-redirect', product_id=product_id)
    else:
        users_product = Product.objects.get(id=product_id)
        try:
            swap = Swap.objects.get((Q(offered_product=users_product) | Q(desired_product=users_product)) & Q(status=SwapStatus.PENDING_CHECKOUT))
            if swap.offered_product == users_product:
                other_users_product = swap.desired_product
            else:
                other_users_product = swap.offered_product
            context = {'users_product': users_product, 'other_users_product': other_users_product}
            return render(request, template_name='checkout/checkout.html', context=context)
        except Swap.DoesNotExist:
            messages.warning(request, 'oops.. looks like this product isn\'t ready for checkout yet')
            return redirect('profile-your-items')


@owns_product
def shipping_address_redirect(request, product_id):

    if request.method == 'POST':
        address_form = ShippingAddressUpdateForm(instance=request.user.profile, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return redirect('pick-collection-time', product_id=product_id)
    else:
        address_form = ShippingAddressUpdateForm(instance=request.user.profile)
        return render(request, 'checkout/shipping_address_redirect.html', context={'address_form': address_form})


@owns_product
def pick_collection_time(request, product_id):

    # Prevent user from accessing this page before prior checkout stages
    if not user_has_valid_address(user=request.user):
        messages.warning(request, 'You must give a valid address first')
        return redirect('checkout', product_id=product_id)

    if request.method == 'POST':
        try:
            selected_time_slot_id = int(request.POST.get('time-slot-radio'))
            return redirect('confirm-payment', product_id=product_id, selected_time_slot_id=selected_time_slot_id)
        except ValueError:
            messages.warning(request, 'select an available time slot')
            return redirect('pick-collection-time', product_id=product_id)  # try again

    else:  # GET request
        max_date_to_show = datetime.date.today() + datetime.timedelta(days=5)
        time_slots = TimeSlot.objects.filter(date__lte=max_date_to_show)  # get all slots within next n days
        time_slots = [slot for slot in time_slots if slot.is_available]
        grouped_time_slots = group_time_slots_by_day(time_slots)
        context = {'product_id': product_id,
                   'grouped_time_slots': grouped_time_slots}
        return render(request, template_name='checkout/pick_collection_time.html', context=context)


@owns_product
def confirm_payment(request, product_id, selected_time_slot_id):

    # Prevent user from accessing this page before prior checkout stages
    try:
        selected_time_slot = TimeSlot.objects.get(id=selected_time_slot_id)
    except TimeSlot.DoesNotExist:
        messages.warning(request, 'time slot does not exist')
        return redirect('profile-your-items')

    if request.method == 'POST':

        # Update product status to CHECKOUT_COMPLETE
        product = Product.objects.get(id=product_id)
        product.status = ProductStatus.CHECKOUT_COMPLETE
        product.save(update_fields=['status'])

        # Update swap status if both products are not CHECKOUT_COMPLETE
        swap = Swap.objects.get((Q(offered_product=product) | Q(desired_product=product))
                                & Q(status=SwapStatus.PENDING_CHECKOUT))
        swap.refresh_status()

        # Create timeslot booking
        booking = create_collection_booking(selected_time_slot=selected_time_slot,
                                            product=product,
                                            swap=swap)
        messages.success(request, f'Swap confirmed - collection booked for {booking.time_slot.day_str} at {booking.time_slot.time.label}')
        return redirect('profile-your-items')

    else:  # GET request
        return render(request, template_name="checkout/confirm_payment.html")







