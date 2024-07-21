from django.contrib.gis.db import models
from django.db.models import Value
from django.db.models.functions import Lower, Replace
from django.utils.text import slugify


class RegionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().defer("geom")

    def get_slug(self, slug):
        return self.annotate(slug=Lower(Replace("nom", Value(" "), Value("-")))).get(
            slug=slug
        )


class Region(models.Model):
    gid = models.BigIntegerField(primary_key=True)
    nom = models.CharField()
    wikipedia = models.CharField()
    code_insee = models.CharField()
    geom = models.MultiPolygonField(srid=3857)

    class Meta:
        managed = False
        db_table = "osm_regions"
        verbose_name = "région"

    objects = RegionManager()

    def __str__(self):
        return self.nom

    def slug(self):
        return slugify(self.nom, allow_unicode=True)
