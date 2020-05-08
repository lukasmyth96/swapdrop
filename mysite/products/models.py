from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy
from django_enumfield import enum
from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image

from .validators import is_square_image


class ProductStatus(enum.Enum):
    LIVE = 0  # live on site
    MATCHED = 1  # successfully matched
    COLLECTED = 2  # successfully picked up by owner
    DELIVERED = 3  # delivered

    __default__ = LIVE

    # InvalidStatusOperationError exception will be raised if we attempt an invalid transition
    __transitions__ = {
        MATCHED: (LIVE,),  # Can go from LIVE to MATCHED
        COLLECTED: (MATCHED,),  # Can go from MATCHED to COLLECTED
        DELIVERED: (COLLECTED,)  # Can go from collected to delivered
    }

    __labels__ = {
        LIVE: ugettext_lazy("Live"),
        MATCHED: ugettext_lazy("Matched"),
        COLLECTED: ugettext_lazy("Collected"),
        DELIVERED: ugettext_lazy("Delivered"),
    }


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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save()

        # Resize to have 512 width whilst maintaining aspect ratio
        img = Image.open(self.image.path)
        ratio = img.size[1] / img.size[0]
        size = (512, int(ratio * 512))
        img = img.resize(size)
        img.save(self.image.path)
