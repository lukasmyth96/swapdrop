from django.contrib import admin

from sizes.models import GenderPreference, PrimarySize, WaistSize, ShoeSize

admin.site.register(GenderPreference)
admin.site.register(PrimarySize)
admin.site.register(WaistSize)
admin.site.register(ShoeSize)

