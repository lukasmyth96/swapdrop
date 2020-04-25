from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})  # FIXME what should this be?