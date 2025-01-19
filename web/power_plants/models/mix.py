from datetime import datetime

from django.contrib.gis.db import models
from django.db import transaction

from parc_elec import odre
from power_plants.models.region import Region
from loguru import logger

NATIONAL_MIX_ENERGY_LABELS = {
    "nucleaire": "Nucléaire",
    "fioul": "Fioul",
    "charbon": "Charbon",
    # "thermique": "Thermique",
    "gaz": "Gaz",
    "bioenergies": "Bioénergies",
    # "eolien": "Éolien",
    "eolien_terrestre": "Éolien terrestre",
    "eolien_offshore": "Éolien en mer",
    "solaire": "Solaire",
    "hydraulique": "Hydraulique",
    "pompage": "Pompage",
    "ech_comm_angleterre": "Échanges le Royaume-Uni",
    "ech_comm_espagne": "Échanges avec l'Espagne",
    "ech_comm_italie": "Échanges avec l'Italie",
    "ech_comm_suisse": "Échanges avec la Suisse",
    "ech_comm_allemagne_belgique": "Échanges avec l'Allemagne et la Belgique",
}

REGIONAL_MIX_ENERGY_LABELS = {
    "nucleaire": "Nucléaire",
    "thermique": "Thermique",
    "bioenergies": "Bioénergies",
    "eolien": "Éolien",
    "solaire": "Solaire",
    "hydraulique": "Hydraulique",
    "pompage": "Pompage",
}

MIX_FAMILIES = {
    "nucleaire": "nuclear",
    "thermique": "fossil",
    "fioul": "fossil",
    "gaz": "fossil",
    "charbon": "fossil",
    "hydraulique": "hydro",
    "tidal": "hydro",
    "eolien_terrestre": "wind",
    "eolien_offshore": "wind",
    "eolien": "wind",
    "solaire": "solar",
    "bioenergies": "fossil",
}

ENERGY_STYLES = {
    "fossil": {"icon": "fire", "color": "#d11500", "background_color": "#d1150088"},
    "nuclear": {"icon": "atom", "color": "#880dbd", "background_color": "#880dbd88"},
    "hydro": {"icon": "water", "color": "#198EC8", "background_color": "#198EC888"},
    "wind": {"icon": "wind", "color": "#118c06", "background_color": "#118c0688"},
    "solar": {"icon": "sun", "color": "#f1b31c", "background_color": "#f1b31c88"},
    "electricity": {
        "icon": "electricity",
        "color": "#828282",
        "background_color": "#82828288",
    },
}


class PowerMixQuerySet(models.QuerySet):
    def national(self):
        return self.filter(insee_code=None)

    def region(self, insee_code):
        return self.filter(insee_code=insee_code)

    def all_types(self):
        qs = self.exclude(production_type__startswith="ech_comm")
        qs = qs.exclude(production_type="pompage")
        return qs

    def as_chart_payload(self):
        if not (objects := list(self)):
            return {"datasets": [], "labels": []}
        
        energy_labels = REGIONAL_MIX_ENERGY_LABELS if objects[0].insee_code else NATIONAL_MIX_ENERGY_LABELS
        order = {key: i for i, key in enumerate(energy_labels.values())}
        logger.debug(order)

        return {
            "datasets": [
                {
                    "label": i.production_type_label,
                    "data": i.values_list[-8:],
                    "backgroundColor": i.colors["background"],
                    "borderColor": i.colors["border"],
                    "fill": "stack",
                }
                for i in sorted(objects, key=lambda object: order.get(object.production_type_label, 0))
            ],
            "labels": objects[0].labels_list[-8:],
        }


class PowerMix(models.Model):
    id = models.AutoField(primary_key=True)
    production_type = models.CharField()
    values = models.JSONField()
    insee_code = models.CharField(null=True, blank=True)

    @classmethod
    def import_from_rte(cls):
        PowerMixImport().bulk_create()

    objects = PowerMixQuerySet.as_manager()

    @property
    def is_national(self):
        return self.insee_code is None

    @property
    def production_type_label(self):
        if self.is_national:
            return NATIONAL_MIX_ENERGY_LABELS[self.production_type]
        else:
            return REGIONAL_MIX_ENERGY_LABELS[self.production_type]

    @property
    def colors(self):
        power_family = MIX_FAMILIES[self.production_type]
        style = ENERGY_STYLES.get(power_family, ENERGY_STYLES["electricity"])
        return {"border": style["color"], "background": style["background_color"]}

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
        rows = []

        national_mix = self.fetch_data_from_eco2mix_national()
        for label in NATIONAL_MIX_ENERGY_LABELS:
            row = {"production_type": label, "values": []}
            for production in national_mix["results"]:
                row["values"].append(
                    {
                        "date": production["date_heure"],
                        "value": int(production[label] or 0),
                    }
                )
            rows.append(row)

        regional_mix = self.fetch_data_from_eco2mix_regional()
        for region in Region.objects.all():
            for label in REGIONAL_MIX_ENERGY_LABELS:
                row = {
                    "production_type": label,
                    "values": [],
                    "insee_code": region.code_insee,
                }
                for production in regional_mix["results"]:
                    if production["code_insee_region"] == region.code_insee:
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
    def fetch_data_from_eco2mix_regional():
        return odre.fetch_eco2mix_regional()

    @staticmethod
    def parse_row(data):
        return {
            "insee_code": data.get("code_insee_region"),
            "production_type": data["production_type"],
            "values": [
                {"date": row["start_date"], "value": row["value"]}
                for row in data["values"]
            ],
        }
