from django.db import models

class PlantRegion(models.Model):
    id = models.AutoField(primary_key=True)
    region_id = models.BigIntegerField()
    plant_id = models.BigIntegerField()

