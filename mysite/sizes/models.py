from django.db import models

from django_enumfield import enum
from sizes.model_enums import GenderOptions, SizeOptions, SizeTypes



class Size(models.Model):
    size = enum.EnumField(SizeOptions)
    size_type = enum.EnumField(SizeTypes)  # primary, waist or shoe
    gender = enum.EnumField(GenderOptions)  # which gender is this size specifically for?


    def __str__(self):
        splitted = self.size.name.split('_')
        size_type = splitted[0]
        if size_type == 'PRIMARY':
            size_text = f'{splitted[1].capitalize()} {splitted[2]}'
        elif size_type == 'WAIST':
            size_text = f'{splitted[1]}\"'
        elif size_type == 'SHOE':
            size_text = f'UK {splitted[1]}'
            if len(splitted) == 3:
                size_text += f'.{splitted[2]}'  # for half sizes
        else:
            raise ValueError('Unhandled size type')
        return size_text


