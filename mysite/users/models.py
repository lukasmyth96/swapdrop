from django.db import models
from django.contrib.auth.models import User

from sizes.models import GenderPreference, PrimarySize, WaistSize, ShoeSize

""" Scroll down for Profile"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 'user' includes: username, password, email address.

    # profile picture
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # shipping address
    house_name_number = models.CharField(max_length=50, blank=True)
    address_line_1 = models.CharField(max_length=50, blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    town_city = models.CharField(max_length=50, blank=True)
    county = models.CharField(max_length=50, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    contact_number = models.CharField(max_length=13, blank=True)

    # clothing preferences
    # Note - this has been designed to allow the user to view a range of sizes rather than limiting them to select only
    # on size
    gender_preference = models.ManyToManyField(GenderPreference)  # menswear, womenswear
    primary_sizes = models.ManyToManyField(PrimarySize)
    waist_sizes = models.ManyToManyField(WaistSize)
    shoe_sizes = models.ManyToManyField(ShoeSize)


    def __str__(self):
        return f'{self.user.username}'










