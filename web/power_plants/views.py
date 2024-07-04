from typing import Optional

from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from power_plants.models import PowerPlant
from power_plants.models import PowerCapacity
from power_plants.models import PowerProduction
from power_plants.models import PowerMix
from power_plants.models import Region
from power_plants.models.plant import ENERGY_STYLES, POWER_PLANT_FAMILIES


def _render_htmx(
    request: HttpRequest, template_name: str, context: Optional[dict] = None
):
    return render(
        request,
        template_name if request.htmx else template_name.replace("html", "page.html"),
        context,
    )


def index(request: HttpRequest):
    mix = PowerMix.objects.national().all_types().as_chart_payload()
    return _render_htmx(
        request,
        "power_plants/index.html",
        context={"families": POWER_PLANT_FAMILIES, "styles": ENERGY_STYLES, "mix": mix},
    )


def about(request: HttpRequest):
    return _render_htmx(request, "power_plants/about.html")


def plant(request: HttpRequest, osm_id: int):
    plant_object = get_object_or_404(PowerPlant, osm_id=osm_id)
    capacities = PowerCapacity.objects.eic(plant_object.eic_list())
    production = PowerProduction.objects.eic(plant_object.eic_list()).as_chart_payload()
    response = _render_htmx(
        request,
        "power_plants/plant.html",
        context={
            "families": POWER_PLANT_FAMILIES,
            "styles": ENERGY_STYLES,
            "plant": plant_object,
            "capacities": capacities,
            "production": production,
        },
    )
    return response


def region(request: HttpRequest, region_slug: str):
    try:
        region_object = Region.objects.get_slug(region_slug)
    except Region.DoesNotExist:
        return HttpResponse(status=404)

    mix = PowerMix.objects.all_types().region(region_object.code_insee).as_chart_payload()
    return _render_htmx(
        request,
        "power_plants/region.html",
        context={
            "families": POWER_PLANT_FAMILIES,
            "styles": ENERGY_STYLES,
            "region": region_object,
            "mix": mix,
        },
    )
