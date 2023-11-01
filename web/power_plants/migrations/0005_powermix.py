# Generated by Django 4.2.5 on 2023-11-01 20:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("power_plants", "0004_powerproduction_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="PowerMix",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("production_type", models.CharField()),
                ("values", models.JSONField()),
            ],
        ),
    ]
