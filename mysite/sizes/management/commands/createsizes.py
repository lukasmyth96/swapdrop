from django.core.management.base import BaseCommand

from sizes.models import PrimarySize, WaistSize, ShoeSize, GenderPreference
from sizes.model_enums import GenderOptions, PrimarySizeOptions, WaistSizeOptions, ShoeSizeOptions


class Command(BaseCommand):

    def handle(self, *args, **options):

        for gender_enum in GenderOptions:
            gender, created_new = GenderPreference.objects.update_or_create(gender=gender_enum)
            if created_new:
                gender.save()
                print(f'Created new gender: {gender}')
            else:
                print(f'Skipping gender: {gender} - already created')


        for size_enum in PrimarySizeOptions:
            gender = GenderOptions.MENSWEAR if size_enum.name.startswith('MEN') else GenderOptions.WOMENSWEAR
            size, created_new = PrimarySize.objects.update_or_create(gender=gender, size=size_enum)
            if created_new:
                size.save()
                print(f'Created new primary size: {size}')
            else:
                print(f'Skipping primary size: {size} - already created')



        for size_enum in WaistSizeOptions:
            size, created_new = WaistSize.objects.update_or_create(size=size_enum)
            if created_new:
                size.save()
                print(f'Created new waist size: {size}')
            else:
                print(f'Skipping waist size: {size} - already created')


        for size_enum in ShoeSizeOptions:
            size, created_new = ShoeSize.objects.update_or_create(size=size_enum)
            if created_new:
                size.save()
                print(f'Created new shoe size: {size}')
            else:
                print(f'Skipping shoe size: {size} - already created')


