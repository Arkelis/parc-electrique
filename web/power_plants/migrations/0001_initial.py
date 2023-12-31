# Generated by Django 4.2.5 on 2023-09-16 20:22

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PowerPlant",
            fields=[
                ("id", models.BigIntegerField()),
                ("osm_id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("output", models.CharField(blank=True, null=True)),
                ("source", models.CharField(blank=True, null=True)),
                ("name", models.CharField(blank=True, null=True)),
                ("short_name", models.CharField(blank=True, null=True)),
                ("wikipedia", models.CharField(blank=True, null=True)),
                ("wikidata", models.CharField(blank=True, null=True)),
                ("operator", models.CharField(blank=True, null=True)),
                ("operator_wikidata", models.CharField(blank=True, null=True)),
                ("operator_wikipedia", models.CharField(blank=True, null=True)),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.MultiPolygonField(
                        blank=True, null=True, srid=4326
                    ),
                ),
            ],
            options={
                "db_table": "osm_power_plants",
                "managed": False,
            },
        ),
    ]
