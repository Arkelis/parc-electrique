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
