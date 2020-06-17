from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import views as auth_views

from dashboard.views import dashboard, UpcomingBookings

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upcoming_bookings/', user_passes_test(lambda u: u.is_superuser)(UpcomingBookings.as_view()), name='upcoming-bookings')
]
