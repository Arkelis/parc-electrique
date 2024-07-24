from django.contrib.gis.db import models
from django.db import transaction
from loguru import logger

from parc_elec.wikidata import fetch_eic_identifiers
from power_plants.models.region import Region
from power_plants.models.plant_region import PlantRegion
from power_plants.models.plant_eic import PlantEic


class PowerPlantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().defer("geometry")


POWER_PLANT_SOURCES = {
    "nuclear": "nucléaire",
    "gas": "gaz",
    "oil": "fioul",
    "biofuel": "bio-carburant",
    "diesel": "diesel",
    "biomass": "biomasse",
    "biogas": "biogaz",
    "geothermal": "géothermique",
    "wind": "éolien",
    "solar": "solaire",
    "waste": "incinération",
    "coal": "charbon",
    "wood": "bois",
    "hydro": "hydraulique",
    "battery": "batteries",
}

POWER_PLANT_FAMILIES = {
    "nuclear": "nuclear",
    "oil": "fossil",
    "gas": "fossil",
    "coal": "fossil",
    "hydro": "hydro",
    "tidal": "hydro",
    "wind": "wind",
    "solar": "solar",
    "waste": "fossil",
}

POWER_PLANT_MIX = {
    "nuclear": "NUCLEAR",
    "oil": "FOSSIL_OIL",
    "gas": "FOSSIL_GAS",
    "coal": "FOSSIL_HARD_COAL",
    "hydro": [
        "HYDRO_PUMPED_STORAGE",
        "HYDRO_RUN_OF_RIVER_AND_POUNDAGE",
        "HYDRO_WATER_RESERVOIR",
    ],
    "tidal": "hydro",
    "wind": "wind",
    "solar": "solar",
    "waste": "fossil",
}

ENERGY_LABELS = {
    "BIOMASS": "biomasse",
    "FOSSIL_GAS": "gaz",
    "FOSSIL_HARD_COAL": "charbon",
    "FOSSIL_OIL": "fioul",
    "HYDRO_PUMPED_STORAGE": "hydraulique step",
    "HYDRO_RUN_OF_RIVER_AND_POUNDAGE": "hydraulique fil de l'eau et éclusée",
    "HYDRO_WATER_RESERVOIR": "hydraulique lacs",
    "NUCLEAR": "nucléaire",
    "SOLAR": "solaire",
    "WASTE": "déchets industriels",
    "WIND_OFFSHORE": "éolien en mer",
    "WIND_ONSHORE": "éolien terrestre",
    "TOTAL": "total",
}

ENERGY_STYLES = {
    "fossil": {"icon": "fire", "color": "#d11500"},
    "nuclear": {"icon": "atom", "color": "#880dbd"},
    "hydro": {"icon": "water", "color": "#198EC8"},
    "wind": {"icon": "wind", "color": "#118c06"},
    "solar": {"icon": "sun", "color": "#f1b31c"},
    "electricity": {"icon": "electricity", "color": "#828282"},
}


class PowerPlant(models.Model):
    # The composite primary key (osm_id, id) found, that is not supported.
    # The first column is selected.
    # id = models.BigIntegerField()
    osm_id = models.BigIntegerField(primary_key=True)
    output = models.CharField(blank=True, null=True)
    source = models.CharField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    short_name = models.CharField(blank=True, null=True)
    wikipedia = models.CharField(blank=True, null=True)
    wikidata = models.CharField(blank=True, null=True)
    operator = models.CharField(blank=True, null=True)
    operator_wikidata = models.CharField(blank=True, null=True)
    operator_wikipedia = models.CharField(blank=True, null=True)
    geometry = models.MultiPolygonField(blank=True, null=True, srid=3857)

    objects = PowerPlantManager()

    class Meta:
        managed = False
        db_table = "power_plants"
        verbose_name = "centrale"

    def __str__(self):
        return self.name or self.short_name or f"Centrale #{self.osm_id}"

    @property
    def eic_list(self):
        plant_eics = PlantEic.objects.filter(plant_id=self.osm_id)
        return list(plant_eics.values_list("eic", flat=True))

    def _sources_as_list(self):
        return self.source.split(";")

    @property
    def icon_path(self):
        main_source = self._sources_as_list()[0]
        energy_family = POWER_PLANT_FAMILIES.get(main_source, "electricity")
        icon_name = ENERGY_STYLES[energy_family]["icon"]
        return f"sprite/{icon_name}.png"

    @property
    def openstreetmap_url(self):
        return (
            f"https://openstreetmap.org/relation/{-self.osm_id}"
            if self.osm_id < 0
            else f"https://openstreetmap.org/way/{self.osm_id}"
        )

    @property
    def wikipedia_url(self):
        page = self.wikipedia.removeprefix("fr:")
        return f"https://fr.wikipedia.org/wiki/{page}"

    @property
    def wikidata_url(self):
        return f"https://wikidata.org/wiki/{self.wikidata}"

    @property
    def production_mode(self):
        display_sources = (
            POWER_PLANT_SOURCES.get(s, s) for s in self._sources_as_list()
        )
        return ", ".join(display_sources)

    @classmethod
    def link_regions(cls):
        plant_regions = PlantRegion.objects.values_list("plant_id")
        for power_plant in cls.objects.exclude(osm_id__in=plant_regions):
            logger.info(f"Assigning power plant {power_plant.name} to a region")
            region = Region.objects.filter(
                geom__intersects=power_plant.geometry
            ).first()

            if region:
                PlantRegion.objects.create(
                    plant_id=power_plant.osm_id, region_id=region.gid
                )
                logger.info(f"Assigned power plant {power_plant.name} to {region.nom}")
            else:
                logger.info(f"No region found for {power_plant.name} ")

    @classmethod
    def link_eic(cls):
        plants_with_wikidata = cls.objects.exclude(wikidata="")
        eic_from_wikidata = fetch_eic_identifiers(
            plants_with_wikidata.values_list("wikidata", flat=True)
        )
        wikidata_to_osm_map = dict(
            plants_with_wikidata.values_list("wikidata", "osm_id")
        )
        eic_to_insert = [
            PlantEic(eic=el.eic, plant_id=wikidata_to_osm_map[el.qid])
            for el in eic_from_wikidata
        ]

        with transaction.atomic():
            PlantEic.objects.all().delete()
            PlantEic.objects.bulk_create(eic_to_insert)
