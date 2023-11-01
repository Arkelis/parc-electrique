from django.contrib.gis.db import models
from django.db.models.expressions import RawSQL

from parc_elec.wikidata import fetch_eic_identifiers


class PowerPlantManager(models.Manager):
    def for_map(self):
        return self.with_normalized_output().with_name()

    def with_normalized_output(self):
        qs = self.annotate(normalized_output=RawSQL("normalize_power(output)", ()))
        qs = qs.exclude(output__in=("", "yes", "no", "inconnu"))
        return qs

    def with_name(self):
        return self.exclude(name="", short_name="")


POWER_PLANT_SOURCES = {
    "nuclear": "nucléaire",
    "gas": "gaz",
    "oil": "fioul",
    "biofuel": "bio-carburant",
    "diesel": "diesel",
    "biomass": "biomasse",
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
    "waste": "fossil"
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
    id = models.BigIntegerField()
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
    geometry = models.MultiPolygonField(blank=True, null=True)

    objects = PowerPlantManager()

    class Meta:
        managed = False
        db_table = "osm_power_plants"
        unique_together = (("osm_id", "id"),)

    def __str__(self):
        return self.name or self.short_name or f"Centrale #{self.osm_id}"

    def eic_list(self):
        """Energy identifier codes fetched from Wikidata"""
        if not (self.wikidata):
            return []

        return fetch_eic_identifiers(self.wikidata)

    def _sources_as_list(self):
        return self.source.split(";")

    @property
    def icon(self):
        main_source = self._sources_as_list()[0]
        energy_family = POWER_PLANT_FAMILIES.get(main_source, "electricity")
        return ENERGY_STYLES[energy_family]["icon"]

    @property
    def openstreetmap_url(self):
        return f"https://openstreetmap.org/way/{self.osm_id}"

    @property
    def wikipedia_url(self):
        page = self.wikipedia.removeprefix("fr:")
        return f"https://fr.wikipedia.org/wiki/{page}"

    @property
    def wikidata_url(self):
        return f"https://wikidata.org/wiki/{self.wikidata}"

    @property
    def production_mode(self):
        display_sources = (POWER_PLANT_SOURCES[s] for s in self._sources_as_list())
        return ", ".join(display_sources)
