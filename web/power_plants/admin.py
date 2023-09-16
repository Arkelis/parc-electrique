from django.contrib import admin

from power_plants.models import PowerPlant


@admin.register(PowerPlant)
class PowerPlantAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'output', 'source']
    search_fields = ["name"]