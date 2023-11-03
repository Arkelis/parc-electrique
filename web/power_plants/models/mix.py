from datetime import datetime

from django.contrib.gis.db import models
from django.db import transaction

from parc_elec import odre

ENERGY_LABELS = {
    "fioul": "Fioul",
    "charbon": "Charbon",
    "gaz": "Gaz",
    "nucleaire": "Nucléaire",
    "eolien_terrestre": "Éolien terrestre",
    "eolien_offshore": "Éolien en mer",
    "solaire": "Solaire",
    "hydraulique": "Hydraulique",
    "pompage": "Pompage",
    "bioenergies": "Bioénergies",
    "ech_comm_angleterre": "Échanges le Royaume-Uni",
    "ech_comm_espagne": "Échanges avec l'Espagne",
    "ech_comm_italie": "Échanges avec l'Italie",
    "ech_comm_suisse": "Échanges avec la Suisse",
    "ech_comm_allemagne_belgique": "Échanges avec l'Allemagne et la Belgique",
}


class PowerMixQuerySet(models.QuerySet):
    def all_types(self):
        qs = self.exclude(production_type__startswith="ech_comm")
        qs = qs.exclude(production_type='pompage')
        return qs

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
        return ENERGY_LABELS[self.production_type]

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
        data = self.fetch_data_from_eco2mix_national()
        rows = []
        for label in ENERGY_LABELS:
            row = {"production_type": label, "values": []}
            for production in data["results"]:
                row["values"].append(
                    {
                        "date": production["date_heure"],
                        "value": int(production[label] or 0),
                    }
                )
            rows.append(row)
        return rows

    @staticmethod
    def fetch_data_from_eco2mix_national():
        return odre.fetch_eco2mix_national()

    @staticmethod
    def parse_row(data):
        return {
            "production_type": data["production_type"],
            "values": [
                {"date": row["start_date"], "value": row["value"]}
                for row in data["values"]
            ],
        }
