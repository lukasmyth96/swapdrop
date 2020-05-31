from django.db import models

from django_enumfield import enum
from sizes.model_enums import GenderOptions, PrimarySizeOptions, WaistSizeOptions, ShoeSizeOptions


class GenderPreference(models.Model):
    gender = enum.EnumField(GenderOptions)

    def __str__(self):
        return self.gender.name


class PrimarySize(models.Model):
    gender = enum.EnumField(GenderOptions)  # which gender is this size specifically for?
    size = enum.EnumField(PrimarySizeOptions)

    def __str__(self):
        gender, size = self.size.name.split('_')
        return f'{gender.lower()} {size}'


class WaistSize(models.Model):
    size = enum.EnumField(WaistSizeOptions)

    def __str__(self):
        inches = self.size.name.split('_')[1]
        return f'{inches}\"'


class ShoeSize(models.Model):
    size = enum.EnumField(ShoeSizeOptions)

    def __str__(self):
        country_code, size_num = self.size.name.split('_')
        return f'{country_code} {size_num}'
