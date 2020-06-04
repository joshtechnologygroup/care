# Generated by Django 2.2.11 on 2020-06-04 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0020_care_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portiecallingdetail',
            name='relation',
            field=models.IntegerField(choices=[(1, 'Self'), (2, 'Father'), (3, 'Mother'), (4, 'Sibling'), (5, 'Spouse'), (6, 'Son'), (7, 'Daughter'), (8, 'Friend'), (9, 'Other relative')], default=1),
        ),
    ]
