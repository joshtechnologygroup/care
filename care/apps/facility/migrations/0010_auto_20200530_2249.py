# Generated by Django 2.2.11 on 2020-05-30 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("facility", "0009_auto_20200530_2150"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalinventory",
            old_name="created_by",
            new_name="updated_by",
        ),
        migrations.RenameField(
            model_name="inventory", old_name="created_by", new_name="updated_by",
        ),
        migrations.AlterUniqueTogether(
            name="inventory", unique_together={("facility", "item")},
        ),
    ]
