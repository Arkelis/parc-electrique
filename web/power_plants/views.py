from typing import Optional

from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from power_plants.models import PowerPlant
from power_plants.models import PowerCapacity
from power_plants.models import PowerProduction
from power_plants.models import PowerMix
from power_plants.models.plant import ENERGY_STYLES, POWER_PLANT_FAMILIES


def _render_htmx(request: HttpRequest, template_name: str, context: Optional[dict] = None):
    return render(
        request,
        template_name if request.htmx else template_name.replace("html", "page.html"),
        context,
    )


def index(request: HttpRequest):
    mix = PowerMix.objects.all_types().as_chart_payload()
    return _render_htmx(
        request,
        "power_plants/index.html",
        context={"families": POWER_PLANT_FAMILIES, "styles": ENERGY_STYLES, "mix": mix},
    )


def about(request: HttpRequest):
    return _render_htmx(request, "power_plants/about.html")


def plant(request: HttpRequest, osm_id: int):
    try:
        plant = get_object_or_404(PowerPlant, osm_id=osm_id)
    except ValueError:
        return HttpResponse(
            f"Plant identifier is expected to be an integer. Given: {osm_id}",
            status=400,
        )
    capacities = PowerCapacity.objects.eic(plant.eic_list())
    production = PowerProduction.objects.eic(plant.eic_list()).as_chart_payload()
    response = _render_htmx(
        request,
        "power_plants/plant.html",
        context={
            "families": POWER_PLANT_FAMILIES,
            "styles": ENERGY_STYLES,
            "plant": plant,
            "capacities": capacities,
            "production": production,
        },
    )
    return response
