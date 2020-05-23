# Generated by Django 2.2.11 on 2020-05-23 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0005_auto_20200524_0050'),
        ('patients', '0002_care_platform'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidSymptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientDisease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PatientSymptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='dailyround',
            name='consultation',
        ),
        migrations.AlterUniqueTogether(
            name='facilitypatientstatshistory',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='facilitypatientstatshistory',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='historicalpatient',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='historicalpatient',
            name='district',
        ),
        migrations.RemoveField(
            model_name='historicalpatient',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='historicalpatient',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpatient',
            name='local_body',
        ),
        migrations.RemoveField(
            model_name='historicalpatient',
            name='nearest_facility',
        ),
        migrations.RemoveField(
            model_name='historicalpatient',
            name='state',
        ),
        migrations.RemoveField(
            model_name='patientconsultation',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='patientconsultation',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='patientconsultation',
            name='referred_to',
        ),
        migrations.RemoveField(
            model_name='patientcontactdetails',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='patientcontactdetails',
            name='patient_in_contact',
        ),
        migrations.RemoveField(
            model_name='patientsampleflow',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='patientsampleflow',
            name='patient_sample',
        ),
        migrations.RemoveField(
            model_name='patientsampletest',
            name='consultation',
        ),
        migrations.RemoveField(
            model_name='patientsampletest',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='patientsampletest',
            name='testing_lab',
        ),
        migrations.DeleteModel(
            name='PatientSearch',
        ),
        migrations.DeleteModel(
            name='PatientConsultationIcmr',
        ),
        migrations.DeleteModel(
            name='PatientIcmr',
        ),
        migrations.DeleteModel(
            name='PatientSampleIcmr',
        ),
        migrations.RemoveIndex(
            model_name='disease',
            name='patients_di_patient_37a9e8_partial',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='active',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='details',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='meta_info',
        ),
        migrations.AddField(
            model_name='disease',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='disease',
            name='name',
            field=models.CharField(default='test', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='govt_id',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='patient',
            name='icmr_id',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='patientfacility',
            name='facility',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='facility.Facility'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patientfacility',
            name='patient_facility_id',
            field=models.CharField(default='1122', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patientfacility',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.Patient'),
        ),
        migrations.AlterUniqueTogether(
            name='patientfacility',
            unique_together={('facility', 'patient_facility_id')},
        ),
        migrations.DeleteModel(
            name='DailyRound',
        ),
        migrations.DeleteModel(
            name='FacilityPatientStatsHistory',
        ),
        migrations.DeleteModel(
            name='HistoricalPatient',
        ),
        migrations.DeleteModel(
            name='PatientConsultation',
        ),
        migrations.DeleteModel(
            name='PatientContactDetails',
        ),
        migrations.DeleteModel(
            name='PatientMetaInfo',
        ),
        migrations.DeleteModel(
            name='PatientSampleFlow',
        ),
        migrations.DeleteModel(
            name='PatientSampleTest',
        ),
        migrations.AddField(
            model_name='patientsymptom',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.Patient'),
        ),
        migrations.AddField(
            model_name='patientsymptom',
            name='symptom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.CovidSymptom'),
        ),
        migrations.AddField(
            model_name='patientdisease',
            name='disease',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.Disease'),
        ),
        migrations.AddField(
            model_name='patientdisease',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.Patient'),
        ),
        migrations.RemoveField(
            model_name='patientfacility',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='patientfacility',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='patientfacility',
            name='other_symptoms',
        ),
        migrations.RemoveField(
            model_name='patientfacility',
            name='reason',
        ),
        migrations.RemoveField(
            model_name='patientfacility',
            name='symptoms',
        ),
        migrations.AddField(
            model_name='patient',
            name='diseases',
            field=models.ManyToManyField(through='patients.PatientDisease', to='patients.Disease'),
        ),
        migrations.AddField(
            model_name='patient',
            name='symptoms',
            field=models.ManyToManyField(through='patients.PatientSymptom', to='patients.CovidSymptom'),
        ),
    ]
