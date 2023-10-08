from django.shortcuts import render
from django.http.request import HttpRequest

from power_plants.models import PowerPlant


async def index(request: HttpRequest):
    return render(request, "power_plants/index.html")


async def plant(request: HttpRequest, gid: int):
    plant = await PowerPlant.objects.aget(osm_id=gid)
    response = render(request, "power_plants/plant.html", context={"plant": plant})
    return response
