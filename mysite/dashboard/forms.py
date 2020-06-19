from django.forms import ModelForm

from bookings.models import Booking


class BookingStatusUpdateForm(ModelForm):

    class Meta:
        model = Booking
        fields = ['status']
