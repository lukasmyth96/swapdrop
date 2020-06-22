import os
from io import BytesIO

from django.db import models
from django.core.files import File
from django.contrib.auth.models import User
from django_enumfield import enum

from PIL import Image

from sizes.models import Size
from sizes.model_enums import GenderOptions

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
    # Note - this has been designed to allow the user to view a range of sizes rather than limiting them to select only one size
    gender_preference = enum.EnumField(GenderOptions, blank=True, null=True)  # menswear, womenswear
    sizes = models.ManyToManyField(Size)

    # Will store image crop dims - filled in ProductCreateView Form
    crop_dimensions_image = None

    def __str__(self):
        return f'{self.user.username}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # FIXME will the lines below cause issues if we update the product??
        self.image = self.crop_resize_rename_image(self.image, self.crop_dimensions_image)
        super(Profile, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def crop_resize_rename_image(self, img_field, crop_dimensions):

        if (not bool(img_field)) or (crop_dimensions is None):
            return img_field  # TODO probably log here if img is not None but crop dims are

        pil_img = Image.open(img_field)
        img_format = pil_img.format  # note - important this comes above rotation

        # Rotate mobile upload images that otherwise get wrong orientation
        exif = pil_img._getexif()
        orientation_key = 274  # cf ExifTags
        if exif and orientation_key in exif:
            orientation = exif[orientation_key]
            rotate_values = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }
            if orientation in rotate_values:
                pil_img = pil_img.transpose(rotate_values[orientation])

        pil_img = pil_img.crop(crop_dimensions)  # crop image
        pil_img = pil_img.resize((512, 512))  # resize image
        thumb_io = BytesIO()  # create a BytesIO object
        pil_img.save(thumb_io, img_format)  # save image to BytesIO object

        image = File(thumb_io, name=self.image.name)  # create a django friendly File object

        return image








