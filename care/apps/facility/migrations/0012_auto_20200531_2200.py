# Generated by Django 2.2.11 on 2020-05-31 16:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0011_merge_20200530_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitystaff',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(code='invalid_mobile', message='Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>', regex='^((\\+91|91|0)[\\- ]{0,1})?[456789]\\d{9}$')]),
        ),
    ]