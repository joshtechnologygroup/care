# Generated by Django 2.2.11 on 2020-06-04 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_care_platform'),
        ('patients', '0019_care_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpatient',
            name='city',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.City'),
        ),
        migrations.AddField(
            model_name='patient',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.City'),
        ),
        migrations.AddField(
            model_name='patientfamily',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.City'),
        ),
    ]
