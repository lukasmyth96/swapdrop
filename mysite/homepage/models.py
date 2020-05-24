from django.db import models
import django


class PotentialUser(models.Model):

    email = models.EmailField()
    date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.email
