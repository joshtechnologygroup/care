# Generated by Django 2.2.11 on 2020-06-08 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0027_auto_20200607_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientfamily',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='patientsampletest',
            name='result',
            field=models.IntegerField(choices=[(1, 'Sample Sent'), (3, 'Positive'), (4, 'Negative'), (5, 'Presumptive Positive'), (6, 'Test Inconclusive')], default=1),
        ),
    ]
