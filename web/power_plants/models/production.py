from datetime import datetime
import json

from django.contrib.gis.db import models
from django.db import transaction

from parc_elec import rte


class PowerProductionManager(models.Manager):
    async def eic(self, eic_list):
        return [c async for c in self.filter(eic__in=eic_list)]


class PowerProduction(models.Model):
    id = models.AutoField(primary_key=True)
    eic = models.CharField()
    name = models.CharField()
    values = models.JSONField()

    @classmethod
    def import_from_rte(cls):
        PowerProductionImport().bulk_create()

    objects = PowerProductionManager()

    @classmethod
    async def as_dataset(cls, eic):
        instances = await cls.objects.eic(eic)

        if not instances:
            return json.dumps({"datasets": [], "labels": []})

        return {
            "datasets": [
                {"label": i.name, "data": i.values_list, "fill": "stack"}
                for i in instances
            ],
            "labels": instances[0].values_list,
        }

    @property
    def values_list(self):
        return [element["value"] for element in self.values]

    @property
    def labels_list(self):
        return [self.datetime_to_hour(element["end_date"]) for element in self.values]

    @staticmethod
    def datetime_to_hour(dt_string):
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%Hh").removeprefix("0")


class PowerProductionImport:
    def bulk_create(self):
        with transaction.atomic():
            PowerProduction.objects.all().delete()
            PowerProduction.objects.bulk_create(
                PowerProduction(**row) for row in self.get_rows()
            )

    def get_rows(self):
        data = self.fetch_data_from_rte()
        return [
            self.parse_row(production)
            for production in data["actual_generations_per_unit"]
        ]

    @staticmethod
    def fetch_data_from_rte():
        return rte.fetch_current_production()

    @staticmethod
    def parse_row(data):
        return {
            "eic": data["unit"]["eic_code"],
            "name": data["unit"]["name"],
            "values": [
                {"date": row["end_date"], "value": row["value"]}
                for row in data["values"]
            ],
        }
