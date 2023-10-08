# Generated by Django 4.2.5 on 2023-10-08 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("power_plants", "0002_powercapacity"),
    ]

    operations = [
        migrations.CreateModel(
            name="PowerProduction",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("eic", models.CharField()),
                ("values", models.JSONField()),
            ],
        ),
    ]
