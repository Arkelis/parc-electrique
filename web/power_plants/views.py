from django.shortcuts import render
from django.http.request import HttpRequest

from power_plants.models import PowerPlant
from power_plants.models import PowerCapacity
from power_plants.models import PowerProduction


def index(request: HttpRequest):
    return render(request, "power_plants/index.html")


def plant(request: HttpRequest, osm_id: int):
    plant = PowerPlant.objects.get(osm_id=osm_id)
    capacities = PowerCapacity.objects.eic(plant.eic_list())
    production = PowerProduction.objects.eic(plant.eic_list()).as_chart_payload()
    response = render(
        request,
        "power_plants/plant.html",
        context={"plant": plant, "capacities": capacities, "production": production},
    )
    return response
