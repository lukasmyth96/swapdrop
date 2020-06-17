from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView

from bookings.models import Booking


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



