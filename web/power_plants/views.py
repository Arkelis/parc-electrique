from typing import Optional

from django.shortcuts import render, get_object_or_404
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.loader import engines
from django.template.loader import get_template
from django.template.exceptions import TemplateSyntaxError

from power_plants.models import PowerPlant
from power_plants.models import PowerCapacity
from power_plants.models import PowerProduction
from power_plants.models import PowerMix
from power_plants.models import Region
from power_plants.models.plant import ENERGY_STYLES, POWER_PLANT_FAMILIES


def _template_from_string(template_str):
    # This function is based on django.template.loader.get_template,
    # but uses Engine.from_string instead of Engine.get_template.
    chain = []
    engine_list = engines.all()
    for engine in engine_list:
        try:
            return engine.from_string(template_str)
        except TemplateSyntaxError as e:
            chain.append(e)
    raise TemplateSyntaxError(template_str, chain=chain)


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
        context={
            "families": POWER_PLANT_FAMILIES,
            "styles": ENERGY_STYLES,
            "mix": mix,
        },
    )


class PanelView:
    def __init_subclass__(cls, template_name: str, show_panel: bool = False):
        cls.show_panel = show_panel
        cls.panel_template = get_template(template_name)
        cls.page_template = _template_from_string(
            f"""
        {{% extends "power_plants/base.html" %}}
        {{% block panel %}}
        {{% include "{template_name}" %}}
        {{% endblock %}}
        """
        )

    def render(self, request, context):
        template = self.panel_template if request.htmx else self.page_template
        context = {"show_panel": self.show_panel, **context}
        return HttpResponse(template.render(context, request))


class IndexView(PanelView, template_name="power_plants/index.html"):
    def __call__(self, request: HttpRequest):
        mix = PowerMix.objects.national().all_types().as_chart_payload()
        return self.render(
            request,
            context={
                "families": POWER_PLANT_FAMILIES,
                "styles": ENERGY_STYLES,
                "mix": mix,
            },
        )


class AboutView(PanelView, template_name="power_plants/about.html", show_panel=True):
    def __call__(self, request: HttpRequest):
        return self.render(
            request,
            context={"show_panel": True},
        )


class PlantView(PanelView, template_name="power_plants/plant.html", show_panel=True):
    def __call__(self, request: HttpRequest, osm_id: int):
        plant_object = get_object_or_404(PowerPlant, osm_id=osm_id)
        eic_identifiers = plant_object.eic_list()
        capacities = PowerCapacity.objects.eic(eic_identifiers)
        production = PowerProduction.objects.eic(eic_identifiers).as_chart_payload()
        region = Region.objects.defer_geometry().get(gid=plant_object.region_id)
        return self.render(
            request,
            context={
                "families": POWER_PLANT_FAMILIES,
                "styles": ENERGY_STYLES,
                "plant": plant_object,
                "capacities": capacities,
                "production": production,
                "region": region,
            },
        )


class RegionView(PanelView, template_name="power_plants/plant.html", show_panel=True):
    def __call__(self, request: HttpRequest, region_slug: str):
        try:
            region_object = Region.objects.defer_geometry().get_slug(region_slug)
        except Region.DoesNotExist:
            return HttpResponse(status=404)

        mix = (
            PowerMix.objects.all_types()
            .region(region_object.code_insee)
            .as_chart_payload()
        )
        return self.render(
            request,
            context={
                "families": POWER_PLANT_FAMILIES,
                "styles": ENERGY_STYLES,
                "region": region_object,
                "mix": mix,
            },
        )
