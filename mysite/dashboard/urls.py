from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import views as auth_views

from dashboard.views import dashboard, UpcomingBookings, BookingDetail, booking_status_update

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upcoming_bookings/', user_passes_test(lambda u: u.is_superuser)(UpcomingBookings.as_view()), name='upcoming-bookings'),
    path('booking_detail/<int:pk>', user_passes_test(lambda u: u.is_superuser)(BookingDetail.as_view()), name='booking-detail'),
    path('booking_status_update<int:booking_id>/', user_passes_test(lambda u: u.is_superuser)(booking_status_update), name='booking-status-update'),
]
