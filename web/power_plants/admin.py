from django.contrib import admin

from power_plants.models import PowerPlant
from power_plants.models import Region


@admin.register(PowerPlant)
class PowerPlantAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'output', 'source']
    search_fields = ["name"]

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['nom']