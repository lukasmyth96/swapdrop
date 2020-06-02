from django.db import models

from django_enumfield import enum
from sizes.model_enums import GenderOptions, SizeOptions, SizeTypes



class Size(models.Model):
    size = enum.EnumField(SizeOptions)
    size_type = enum.EnumField(SizeTypes)  # primary, waist or shoe
    gender = enum.EnumField(GenderOptions)  # which gender is this size specifically for?


    def __str__(self):
        return self.size

