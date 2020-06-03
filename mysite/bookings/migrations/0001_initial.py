# Generated by Django 3.0.5 on 2020-06-02 07:03

import bookings.model_enums
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_enumfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', django_enumfield.db.fields.EnumField(enum=bookings.model_enums.Slot)),
                ('date', models.DateField(default=datetime.date.today)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_type', django_enumfield.db.fields.EnumField(enum=bookings.model_enums.BookingType)),
                ('date_booked', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.TimeSlot')),
            ],
        ),
    ]
