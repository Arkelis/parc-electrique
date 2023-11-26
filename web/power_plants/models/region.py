from django.contrib.gis.db import models

class Region(models.Model):
    # The composite primary key (osm_id, id) found, that is not supported.
    # The first column is selected.
    gid = models.BigIntegerField(primary_key=True)
    nom = models.CharField()
    wikipedia = models.CharField()
    code_insee = models.CharField()
    geom = models.MultiPolygonField(srid=3857)

    class Meta:
        managed = False
        db_table = "osm_regions"
        verbose_name = 'région'

    def __str__(self):
        return self.nom