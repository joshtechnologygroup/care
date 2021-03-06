# Generated by Django 2.2.11 on 2020-05-22 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("facility", "0001_care_platform"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ambulance", options={"verbose_name_plural": "ambulances"},
        ),
        migrations.AlterModelOptions(
            name="ambulancedriver",
            options={"verbose_name_plural": "AmbulancesDrivers"},
        ),
        migrations.AlterModelOptions(
            name="facilitylocalgovtbody",
            options={"verbose_name_plural": "FacilityLocalGovtBodies"},
        ),
        migrations.RemoveConstraint(
            model_name="facilitylocalgovtbody",
            name="cons_facilitylocalgovtbody_only_one_null",
        ),
    ]
