# Generated by Django 2.2.11 on 2020-05-30 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("patients", "0010_patienttransfer"),
    ]

    operations = [
        migrations.RemoveField(model_name="historicalpatient", name="year_of_birth",),
        migrations.RemoveField(model_name="patient", name="year_of_birth",),
    ]
