from django.db import models

class PlantEic(models.Model):
    id = models.AutoField(primary_key=True)
    eic = models.CharField()
    plant_id = models.BigIntegerField()

