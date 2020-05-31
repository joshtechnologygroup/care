from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin
from apps.patients import models
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class PatientSymptomInline(admin.TabularInline):
    model = models.PatientSymptom
    min_num = 0
    extra = 1


class PatientDiseaseInline(admin.TabularInline):
    model = models.PatientDisease
    min_num = 0
    extra = 1


class PatientResource(resources.ModelResource):
    class Meta:
        model = models.Patient
        fields = (
            "id",
            "icmr_id",
            "govt_id",
            "name",
            "active",
            "address",
            "district",
            "state",
            "pincode",
            "source",
            "nearest_facility",
            "month",
            "year",
            "gender",
            "phone_number",
            "phone_number_belongs_to",
            "date_of_birth",
            "nationality",
            "is_medical_worker",
            "blood_group",
            "contact_with_confirmed_carrier",
            "contact_with_suspected_carrier",
            "past_travel",
            "countries_travelled_old",
            "countries_travelled",
            "present_health",
            "ongoing_medication",
            "has_SARI",
            "number_of_aged_dependents",
            "number_of_chronic_diseased_dependents",
            "created_by",
            "is_active",
            "portea_able_to_connect",
            "symptoms",
            "diseases",
            "covid_status",
            "clinical_status",
            "patient_status",
            "created_at",
            "updated_at",
        )


class PatientAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    resource_class = PatientResource
    list_display = ("id", "name", "gender")
    inlines = [
        PatientSymptomInline,
        PatientDiseaseInline,
    ]
    djangoql_completion_enabled_by_default = True


class PatientSampleAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    djangoql_completion_enabled_by_default = True


class DiseaseAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    model = models.Disease
    djangoql_completion_enabled_by_default = True


class CovidSymptomAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    model = models.CovidSymptom
    djangoql_completion_enabled_by_default = True


class PatientStatusAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    model = models.PatientStatus
    djangoql_completion_enabled_by_default = True


class PatientCovidStatusStatusAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    model = models.CovidStatus
    djangoql_completion_enabled_by_default = True


class PatientClinicalStatusStatusAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    model = models.ClinicalStatus
    djangoql_completion_enabled_by_default = True


class PatientTransferAdmin(ImportExportModelAdmin):
    raw_id_fields = (
        "from_patient_facility",
        "to_facility",
    )
    list_display = (
        "__str__",
        "status",
    )
    list_filter = ("status",)
    search_fields = ("from_patient_facility__patient__name",)


class PatientFacilityAdmin(admin.ModelAdmin):
    raw_id_fields = (
        "patient",
        "facility",
    )
    list_display = ("patient", "facility", "patient_status")
    list_filter = ("patient_status",)
    search_fields = ("patient__name",)


admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.PatientFacility, PatientFacilityAdmin)
admin.site.register(models.Disease, DiseaseAdmin)
admin.site.register(models.PatientGroup, ImportExportModelAdmin)
admin.site.register(models.CovidSymptom, CovidSymptomAdmin)
admin.site.register(models.PatientStatus, PatientStatusAdmin)
admin.site.register(models.CovidStatus, PatientCovidStatusStatusAdmin)
admin.site.register(models.ClinicalStatus, PatientClinicalStatusStatusAdmin)
admin.site.register(models.PatientTimeLine)
admin.site.register(models.PatientFamily)
admin.site.register(models.PortieCallingDetail)
admin.site.register(models.PatientSampleTest)
admin.site.register(models.PatientTransfer, PatientTransferAdmin)
