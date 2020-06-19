import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_enumfield import enum

from .model_enums import Slot, BookingType, BookingStatus
from products.models import Product, ProductStatus


class TimeSlot(models.Model):

    time = enum.EnumField(Slot)
    date = models.DateField(default=datetime.date.today)
    # capacity = total number of collections/deliveries that this slot can handle - NOT the remaining availability
    capacity = models.PositiveIntegerField()

    def __str__(self):
        date_string = self.date.strftime('%A %d %B')
        time_string = self.time.label
        return f'{date_string} @{time_string}'

    @property
    def day_str(self):
        """ Returns e.g. Mon, Tue etc."""
        return self.date.strftime('%a')

    @property
    def date_str(self):
        """ Returns e.g. 5th, 3rd etc."""
        date_suffix = {
                1: 'st',
                2: 'nd',
                3: 'rd',
                21: 'st',
                22: 'nd',
                23: 'rd',
                31: 'st'
            }
        suffix = date_suffix.get(self.date.day, 'th')
        return f'{self.date.day}{suffix}'



    @property
    def bookings(self):
        """ Returns QuerySet of bookings in this time slot"""
        return Booking.objects.filter(time_slot=self)

    @property
    def num_bookings(self):
        return len(self.bookings)

    @property
    def is_available(self):
        """ Returns True if number of bookings < capacity and time slot date is after current date"""
        return (self.num_bookings < self.capacity) and (datetime.date.today() < self.date)


class Booking(models.Model):

    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    booking_type = enum.EnumField(BookingType)
    status = enum.EnumField(BookingStatus, default=BookingStatus.PENDING)
    date_booked = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.time_slot.__str__()} - {self.booking_type.label} from \'{self.owner.username}\' - status: {self.status.name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ Update status of product once booking marked as complete"""
        if self.status == BookingStatus.COMPLETE:
            if self.booking_type == BookingType.COLLECTION:
                self.product.status = ProductStatus.COLLECTED
            elif self.booking_type == BookingType.DELIVERY:
                self.product.status = ProductStatus.DELIVERED
            self.product.save(update_fields=['status'])
        return super(Booking, self).save(force_insert, force_update, using, update_fields)










