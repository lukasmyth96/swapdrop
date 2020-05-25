from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 'user' includes: username, password, email address.

    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    house_name_number = models.CharField(max_length=50, blank=True)
    address_line_1 = models.CharField(max_length=50, blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    town_city = models.CharField(max_length=50, blank=True)
    county = models.CharField(max_length=50, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    contact_number = models.CharField(max_length=13, blank=True)

    def __str__(self):
        return f'{self.user.username}'









