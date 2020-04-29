from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image


class Product(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

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
