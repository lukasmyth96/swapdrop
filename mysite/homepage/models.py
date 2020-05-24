from django.db import models
from django.utils import timezone


class PotentialUser(models.Model):

    email = models.EmailField()
    date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.email
