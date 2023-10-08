from django.shortcuts import render
from django.http.request import HttpRequest

from power_plants.models import PowerPlant
from power_plants.models import PowerCapacity
from power_plants.models import PowerProduction


async def index(request: HttpRequest):
    return render(request, "power_plants/index.html")


async def plant(request: HttpRequest, osm_id: int):
    plant = await PowerPlant.objects.aget(osm_id=osm_id)
    capacities = await PowerCapacity.objects.eic(plant.eic_list())
    production = await PowerProduction.objects.eic(plant.eic_list())
    response = render(
        request,
        "power_plants/plant.html",
        context={"plant": plant, "capacities": capacities, "production": production},
    )
    return response
