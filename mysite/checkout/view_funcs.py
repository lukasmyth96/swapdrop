import datetime

from django.db.models import Q

from users.forms import ShippingAddressUpdateForm
from products.models import Product
from swaps.models import Swap
from swaps.models import SwapStatus
from bookings.models import TimeSlot, Booking
from bookings.model_enums import BookingType


def user_has_valid_address(user):
    """ Return True if this user already has a valid address, False otherwise"""
    address_form = ShippingAddressUpdateForm(instance=user.profile)
    return address_form.is_initial_valid()


def user_has_booked_pickup_time(product_id):
    """ Return True if user has made collection booking for product, False otherwise"""
    product = Product.objects.get(id=product_id)
    try:
        Booking.objects.get(product=product, booking_type=BookingType.COLLECTION)
        return True
    except Booking.DoesNotExist:
        return False


def group_time_slots_by_day(time_slots):
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


def create_collection_booking(selected_time_slot, product, swap):
    """ Create and save collection Booking in chosen time slot"""
    booking = Booking(time_slot=selected_time_slot,
                      owner=product.owner,
                      product=product,
                      swap=swap,
                      booking_type=BookingType.COLLECTION)
    booking.save()
    return booking
