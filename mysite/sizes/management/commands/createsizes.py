from django.core.management.base import BaseCommand

from sizes.models import Size
from sizes.model_enums import GenderOptions, SizeTypes, SizeOptions


class Command(BaseCommand):

    def handle(self, *args, **options):

        for size_enum in SizeOptions:

            # Which gender(s) does the size apply to?
            if 'WOMEN' in size_enum.name:  # MUST have if on WOMEN first because 'MEN' is in both
                gender = GenderOptions.WOMENSWEAR
            elif 'MEN' in size_enum.name:
                gender = GenderOptions.MENSWEAR
            else:
                gender = GenderOptions.UNISEX

            # Which type of size is it?
            if size_enum.name.startswith('PRIMARY'):
                size_type = SizeTypes.PRIMARY
            elif size_enum.name.startswith('WAIST'):
                size_type = SizeTypes.WAIST
            elif size_enum.name.startswith('SHOE'):
                size_type = SizeTypes.SHOE
            else:
                raise ValueError(f'Unhandled size type: {size_enum.name}')

            # Create Size object if doesn't exist already
            size, created_new = Size.objects.update_or_create(size=size_enum, size_type=size_type, gender=gender)
            if created_new:
                size.save()
                print(f'Created new primary size: {size}')
            else:
                print(f'Skipping primary size: {size} - already created')




