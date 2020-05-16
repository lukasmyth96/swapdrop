from django.db import models
from django.apps import apps
from django.utils import timezone
from django_enumfield import enum
from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image

from swaps.model_enums import SwapStatus
from .model_enums import ProductStatus
from .validators import is_square_image


class Product(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    image = models.ImageField(default='default.jpg', upload_to='product_pics', validators=[is_square_image])
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = enum.EnumField(ProductStatus, default=ProductStatus.LIVE)

    def __str__(self):
        return f'{self.name} - status:{self.status.name}'

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    @property
    def number_of_offers(self):
        """ Returns number of pending offers currently for this product

        Note - using apps.get_model() to avoid circular import
        """
        Swap = apps.get_model('swaps', 'Swap')
        return len(Swap.objects.filter(desired_product=self, status=SwapStatus.PENDING_REVIEW))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save()

        # Resize to have 512*512
        img = Image.open(self.image.path)
        size = (512, 512)
        img = img.resize(size)
        img.save(self.image.path)
