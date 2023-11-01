from datetime import datetime

from django.contrib.gis.db import models
from django.db import transaction

from parc_elec import rte

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


class PowerMixQuerySet(models.QuerySet):
    def all_types(self):
        return self.exclude(production_type="TOTAL")

    def as_chart_payload(self):
        if not self:
            return {"datasets": [], "labels": []}

        return {
            "datasets": [
                {
                    "label": i.production_type_label,
                    "data": i.values_list[-8:],
                    "fill": "stack",
                }
                for i in self.iterator()
            ],
            "labels": self.first().labels_list[-8:],
        }


class PowerMix(models.Model):
    id = models.AutoField(primary_key=True)
    production_type = models.CharField()
    values = models.JSONField()

    @classmethod
    def import_from_rte(cls):
        PowerMixImport().bulk_create()

    objects = PowerMixQuerySet.as_manager()

    @property
    def production_type_label(self):
        return ENERGY_LABELS[self.production_type].capitalize()

    @property
    def values_list(self):
        return [abs(element["value"]) for element in self.values]

    @property
    def labels_list(self):
        return [self.datetime_to_hour(element["date"]) for element in self.values]

    @staticmethod
    def datetime_to_hour(dt_string):
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%Hh").removeprefix("0")


class PowerMixImport:
    def bulk_create(self):
        with transaction.atomic():
            PowerMix.objects.all().delete()
            PowerMix.objects.bulk_create(PowerMix(**row) for row in self.get_rows())

    def get_rows(self):
        data = self.fetch_data_from_rte()
        return [
            self.parse_row(production)
            for production in data["actual_generations_per_production_type"]
        ]

    @staticmethod
    def fetch_data_from_rte():
        return rte.fetch_current_production_mix()

    @staticmethod
    def parse_row(data):
        return {
            "production_type": data["production_type"],
            "values": [
                {"date": row["end_date"], "value": row["value"]}
                for row in data["values"]
            ],
        }
