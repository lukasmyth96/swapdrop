from django.db import models
from django.apps import apps
from django.utils import timezone
from django_enumfield import enum
from django.contrib.auth.models import User
from django.urls import reverse

from io import BytesIO
from django.core.files import File
from PIL import Image

from swaps.model_enums import SwapStatus
from sizes.models import Size
from sizes.model_enums import GenderOptions
from .model_enums import ProductStatus, ClothingType
from .validators import is_square_image


class Product(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    gender = enum.EnumField(GenderOptions, default=GenderOptions.UNISEX)
    clothing_type = enum.EnumField(ClothingType, default=ClothingType.T_SHIRT)
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(default='default.jpg', upload_to='product_pics', validators=[is_square_image])
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = enum.EnumField(ProductStatus, default=ProductStatus.LIVE)

    def __str__(self):
        return f'ID: {self.id} - {self.name} - status:{self.status.name}'

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print('stop here')
        self.image = self.crop_image()
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def crop_image(self):
        im = Image.open(self.image)
        cropped_dimensions = tuple(self.cropped_dimensions)  # this attribute gets added in ProductCreateForm.save

        im.convert('RGB')  # convert mode
        im = im.crop(cropped_dimensions)  # resize image
        thumb_io = BytesIO()  # create a BytesIO object
        im.save(thumb_io, 'JPEG', quality=85)  # save image to BytesIO object
        image = File(thumb_io, name=self.image.name)  # create a django friendly File object

        return image

    @property
    def number_of_offers(self):
        """ Returns number of pending offers currently for this product

        Note - using apps.get_model() to avoid circular import
        """
        Swap = apps.get_model('swaps', 'Swap')
        return len(Swap.objects.filter(desired_product=self, status=SwapStatus.PENDING_REVIEW))

