from django.contrib.gis.db import models
from django.db.models.expressions import RawSQL


class PowerPlantManager(models.Manager):
    def with_normalized_output(self):
        qs = self.annotate(normalized_output=RawSQL("normalize_power(output)", ()))
        qs = qs.exclude(output__in=("", "yes", "no", "inconnu"))
        return qs


class PowerPlant(models.Model):
    # The composite primary key (osm_id, id) found, that is not supported.
    # The first column is selected.
    id = models.AutoField()
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
