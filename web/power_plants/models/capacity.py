from django.contrib.gis.db import models
from django.db import transaction

from parc_elec import rte


class PowerCapacityManager(models.Manager):
    def eic(self, eic_list):
        return self.filter(eic__in=eic_list)


class PowerCapacity(models.Model):
    id = models.AutoField(primary_key=True)
    eic = models.CharField()
    name = models.CharField()
    output = models.CharField()  # in MW
    source = models.CharField()

    @classmethod
    def import_from_rte(cls):
        PowerCapacityImport().bulk_create()

    objects = PowerCapacityManager()


class PowerCapacityImport:
    def bulk_create(self):
        with transaction.atomic():
            PowerCapacity.objects.all().delete()
            PowerCapacity.objects.bulk_create(
                PowerCapacity(**row) for row in self.get_rows()
            )

    def get_rows(self):
        data = self.fetch_data_from_rte()
        return [
            self.parse_row(capacity)
            for capacity in data["capacities_per_production_unit"]
        ]

    @staticmethod
    def fetch_data_from_rte():
        return rte.fetch_current_installed_capacity()

    @staticmethod
    def parse_row(data):
        return {
            "eic": data["production_unit"]["code_eic"],
            "name": data["production_unit"]["name"],
            "output": data["values"][-1]["installed_capacity"],
            "source": data["values"][-1]["type"],
        }
