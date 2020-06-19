from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, FormView

from bookings.models import Booking
from dashboard.forms import BookingStatusUpdateForm


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    return render(request, template_name='dashboard/dashboard.html')


class UpcomingBookings(ListView):
    model = Booking
    template_name = 'dashboard/upcoming_bookings.html'
    context_object_name = 'bookings'


class BookingDetail(DetailView):
    model = Booking
    template_name = 'dashboard/booking_detail.html'
    context_object_name = 'booking'

    def get_context_data(self, **kwargs):
        context = super(BookingDetail, self).get_context_data(**kwargs)
        context['form'] = BookingStatusUpdateForm(instance=self.object)
        return context


def booking_status_update(request, booking_id):
    """ Update the status of a single booking and the product it corresponds to"""
    if request.method == 'POST':
        booking = Booking.objects.get(id=booking_id)
        form = BookingStatusUpdateForm(instance=booking, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking completed')
        else:
            messages.warning(request, 'Something went wrong!')
        return redirect('upcoming-bookings')







