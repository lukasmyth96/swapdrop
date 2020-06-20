from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, FormView

from swaps.models import Swap, SwapStatus
from bookings.models import Booking, BookingStatus, BookingType
from dashboard.forms import BookingStatusUpdateForm


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    return render(request, template_name='dashboard/dashboard.html')


class UpcomingBookings(ListView):
    model = Booking
    template_name = 'dashboard/upcoming_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(status=BookingStatus.PENDING)


class BookingDetail(DetailView):
    model = Booking
    template_name = 'dashboard/booking_detail.html'
    context_object_name = 'booking'

    def get_context_data(self, **kwargs):
        context = super(BookingDetail, self).get_context_data(**kwargs)
        context['form'] = BookingStatusUpdateForm(instance=self.object)
        return context


def booking_status_update(request, booking_id):
    """
    Receives submitted form to update status of a booking at the product it corresponds to.
    Parameters
    ----------
    request
    booking_id

    Returns
    -------

    """
    if request.method == 'POST':
        booking = Booking.objects.get(id=booking_id)
        form = BookingStatusUpdateForm(instance=booking, data=request.POST)
        if form.is_valid():
            form.save()
            new_booking_status = form.cleaned_data.get('status')
            messages.success(request, f'Updated booking status to {new_booking_status.name}')

            # If collection marked as complete then auto create a delivery booking for that product
            if (booking.booking_type == BookingType.COLLECTION) and (new_booking_status == BookingStatus.COMPLETE):
                try:
                    _create_delivery_booking(product=booking.product, swap=booking.swap)
                    messages.success(request, 'Created delivery booking for this product')
                except Exception as err:
                    messages.warning(request, f'Error - failed to create delivery booking for this product: {err}')
        else:
            messages.warning(request, 'Something went wrong!')
        return redirect('upcoming-bookings')


def _create_delivery_booking(product, swap):
    """
    Create a delivery booking for a given product where the owner of the booking will be the user who will be receving
    the product.

    This is used to automatically create delivery booking once a product is marked as collected
    Parameters
    ----------
    product

    Returns
    -------

    """

    if swap.offered_product == product:
        other_product = swap.desired_product
    else:
        other_product = swap.offered_product

    user_to_deliver_to = other_product.owner
    booking = Booking(time_slot=None,
                      product=product,
                      swap=swap,
                      owner=user_to_deliver_to,
                      booking_type=BookingType.DELIVERY)
    booking.save()












