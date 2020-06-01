from datetime import datetime

from django.utils.translation import ugettext as _
from rest_framework import serializers as rest_serializers
from rest_framework import exceptions as rest_exceptions
from apps.commons import constants as commons_constants
from apps.patients import (
    constants as patient_constants,
    models as patient_models,
)
from apps.facility import models as facility_models


class PatientFacilitySerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.PatientFacility
        fields = (
            "patient_status",
            "facility",
            "patient_facility_id",
        )
        read_only_fields = ("facility",)


class GenderField(rest_serializers.RelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        if value == 1:
            return "Male"
        if value == 2:
            return "Female"
        else:
            return "Others"


class PatientListSerializer(rest_serializers.ModelSerializer):
    patient_status = rest_serializers.SerializerMethodField()
    gender = GenderField(queryset=patient_models.Patient.objects.none())
    ownership_type = rest_serializers.CharField(read_only=True)
    facility_type = rest_serializers.CharField(read_only=True)
    facility_name = rest_serializers.CharField(read_only=True)
    facility_district = rest_serializers.CharField(read_only=True)

    class Meta:
        model = patient_models.Patient
        fields = (
            "id",
            "icmr_id",
            "govt_id",
            "name",
            "gender",
            "year",
            "month",
            "phone_number",
            "phone_number_belongs_to",
            "address",
            "district",
            "cluster_group",
            "patient_status",
            "covid_status",
            "clinical_status",
            "clinical_status_updated_at",
            "portea_called_at",
            "portea_able_to_connect",
            "facility_name",
            "facility_district",
            "facility_type",
            "ownership_type",
            "native_state",
            "native_country",
            "pincode",
        )
        extra_kwargs = {
            "facility": {"required": True},
            "nearest_facility": {"required": True},
            "state": {"required": True},
            "district": {"required": True},
        }
        read_only_fields = (
            "symptoms",
            "diseases",
        )

    def get_patient_status(self, instance):
        if instance.patient_status == patient_constants.FACILITY_STATUS:
            return instance.facility_status
        return instance.patient_status


class PatientGroupSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.PatientGroup
        fields = (
            "id",
            "name",
            "description",
            "created_at",
        )
        read_only_fields = ("created_at",)


class CovidStatusSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.CovidStatus
        fields = (
            "id",
            "name",
            "description",
        )


class ClinicalStatusSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.ClinicalStatus
        fields = (
            "id",
            "name",
            "description",
        )


class PatientStatusSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.PatientStatus
        fields = ("id", "name", "description")


class PatientTimeLineSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.PatientTimeLine
        fields = (
            "date",
            "description",
        )


class PortieCallingDetailSerialzier(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.PortieCallingDetail
        fields = (
            "id",
            "portie",
            "patient",
            "patient_family",
            "called_at",
            "able_to_connect",
            "able_to_connect",
            "comments",
        )

    def validate_patient(self, patient):
        if patient.patient_status != patient_constants.HOME_ISOLATION:
            raise rest_serializers.ValidationError(_("Calling detail can be added only for home Isolated patient."))
        return patient


class PatientSampleTestSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.PatientSampleTest
        fields = (
            "id",
            "patient",
            "testing_lab",
            "doctor_name",
            "result",
            "date_of_sample",
            "date_of_result",
            "status_updated_at",
        )


class PatientTransferFacilitySerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.Facility
        fields = (
            "facility_code",
            "name",
        )


class PatientTransferPatientSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.Patient
        fields = (
            "icmr_id",
            "govt_id",
            "name",
            "gender",
            "month",
            "year",
            "phone_number",
        )


class PatientTransferSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for patient transfer related details
    """

    patient_name = rest_serializers.CharField(source="from_patient_facility.patient.name")
    icmr_id = rest_serializers.CharField(source="from_patient_facility.patient.icmr_id")
    govt_id = rest_serializers.CharField(source="from_patient_facility.patient.govt_id")
    gender = rest_serializers.CharField(source="from_patient_facility.patient.gender")
    month = rest_serializers.CharField(source="from_patient_facility.patient.month")
    year = rest_serializers.CharField(source="from_patient_facility.patient.year")
    phone_number = rest_serializers.CharField(source="from_patient_facility.patient.phone_number")
    from_facility_id = rest_serializers.CharField(source="from_patient_facility.facility.facility_code")
    from_facility_name = rest_serializers.CharField(source="from_patient_facility.facility.name")
    to_facility_id = rest_serializers.CharField(source="to_facility.facility_code")
    to_facility_name = rest_serializers.CharField(source="to_facility.name")
    requested_at = rest_serializers.DateTimeField(source="created_at", format="%m/%d/%Y %I:%M %p")
    status_updated_at = rest_serializers.DateTimeField(format="%m/%d/%Y %I:%M %p")

    class Meta:
        model = patient_models.PatientTransfer
        fields = (
            "icmr_id",
            "govt_id",
            "patient_name",
            "gender",
            "month",
            "year",
            "phone_number",
            "from_facility_id",
            "from_facility_name",
            "to_facility_name",
            "to_facility_id",
            "requested_at",
            "status",
            "status_updated_at",
        )


class PatientTransferUpdateSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for updating status related details about Patient transfer
    """

    class Meta:
        model = patient_models.PatientTransfer
        fields = (
            "status",
            "status_updated_at",
            "comments",
        )

    def validate_status(self, status):
        if status == self.instance.status:
            return status

        final_statuses = [
            patient_constants.TRANSFER_STATUS.REJECTED,
            patient_constants.TRANSFER_STATUS.ACCEPTED,
        ]
        initial_status = [
            patient_constants.TRANSFER_STATUS.PENDING,
            patient_constants.TRANSFER_STATUS.WITHDRAW,
        ]

        if self.instance.status in final_statuses and status not in final_statuses:
            raise rest_serializers.ValidationError(_(f"{self.instance.status} status can not be converted into {status}"))
    
        """
        1. From facility user can only move from pending to withdraw OR withdraw to pending
        2. To Facility member can do anything except pending to withdraw and withdraw to pending
        """
        current_user = self.context['request'].user
        if current_user.user_type and current_user.user_type.name == commons_constants.FACILITY_MANAGER:
            # When user does not belongs to from and to facility then he can not update anything
            if not current_user.facilityuser_set.filter(
                facility_id__in=[self.instance.to_facility.id, self.instance.from_facility.facility.id]
            ).exists():
                raise rest_serializers.ValidationError(
                    _("You do not have permission to update this transfer status")
                )
            # When user does not belongs to to-facility then he can not update final status
            elif not current_user.facilityuser_set.filter(facility=self.instance.to_facility).exists():
                if self.instance.status in final_statuses or status in final_statuses:
                    raise rest_serializers.ValidationError(_("You do not have permission to change current status"))
            # When user does not belongs to from-facility then he move from one initial status to other initial status
            elif not current_user.facilityuser_set.filter(facility=self.instance.from_facility.facility).exists():
                if self.instance.status in initial_status and status in initial_status:
                    raise rest_serializers.ValidationError(_("You do not have permission to change current status"))
        elif current_user.user_type and current_user.user_type.name == commons_constants.PORTEA:
            raise rest_serializers.ValidationError(_("You do not have permission to change current status"))

        return status

    def update(self, instance, validated_data):
        if validated_data.get("status") != instance.status:
            validated_data["status_updated_at"] = datetime.now()
        return super().update(instance, validated_data)


class PatientFamilySerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.PatientFamily
        fields = ("name", "relation", "age_year", "age_month", "gender", "phone_number")


class PortieCallingDetailSerializer(rest_serializers.ModelSerializer):
    name = rest_serializers.SerializerMethodField()
    portie_phone_number = rest_serializers.SerializerMethodField()
    patient_contact_number = rest_serializers.SerializerMethodField()
    patient_relation = rest_serializers.SerializerMethodField()
    status = rest_serializers.SerializerMethodField()

    def get_name(self, instance):
        return instance.portie.name

    def get_portie_phone_number(self, instance):
        return instance.portie.phone_number

    def get_patient_contact_number(self, instance):
        return instance.patient.phone_number

    def get_patient_relation(self, instance):
        return instance.patient_family.relation if instance.patient_family else "Self"

    def get_status(self, instance):
        return instance.able_to_connect

    class Meta:
        model = patient_models.PortieCallingDetail
        fields = (
            "name",
            "portie_phone_number",
            "status",
            "patient_contact_number",
            "patient_relation",
            "status",
            "comments",
        )


class ContactDetailsSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = patient_models.Patient
        fields = (
            "phone_number",
            "address",
            "district",
            "state",
            "phone_number_belongs_to",
            "local_body",
        )


class MedicationDetailsSerializer(rest_serializers.ModelSerializer):
    attendant_name = rest_serializers.SerializerMethodField()
    attendant_email = rest_serializers.SerializerMethodField()
    attendant_phone_number = rest_serializers.SerializerMethodField()

    def get_attendant_name(self, instance):
        return ""

    def get_attendant_email(self, instance):
        return ""

    def get_attendant_phone_number(self, instance):
        return ""

    class Meta:
        model = patient_models.Patient
        fields = (
            "symptoms",
            "diseases",
            "covid_status",
            "clinical_status",
            "attendant_name",
            "attendant_email",
            "attendant_phone_number",
        )


class PatientFacilityDetailsSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.Facility
        fields = ("id", "name", "district", "facility_type", "owned_by")


class PatientLabSerializer(rest_serializers.ModelSerializer):
    name = rest_serializers.SerializerMethodField()
    code = rest_serializers.SerializerMethodField()

    def get_name(self, instance):
        testing_lab = facility_models.TestingLab.objects.filter(id=instance.testing_lab.id)
        return testing_lab.first().name if testing_lab else ""

    def get_code(self, instance):
        testing_lab = facility_models.TestingLab.objects.filter(id=instance.testing_lab.id)
        return testing_lab.first().code if testing_lab else ""

    class Meta:
        model = patient_models.PatientSampleTest
        fields = (
            "name",
            "code",
            "date_of_sample",
            "result",
            "status_updated_at",
        )


class PersonalDetailsSerializer(rest_serializers.ModelSerializer):
    age_years = rest_serializers.IntegerField(source="year")
    age_months = rest_serializers.IntegerField(source="month")

    class Meta:
        model = patient_models.Patient
        fields = (
            "name",
            "icmr_id",
            "govt_id",
            "gender",
            "cluster_group",
            "age_years",
            "age_months",
        )


class PatientDetailsSerializer(rest_serializers.Serializer):
    personal_details = rest_serializers.SerializerMethodField()
    patient_family_details = rest_serializers.SerializerMethodField()
    portie_calling_details = rest_serializers.SerializerMethodField()
    contact_details = rest_serializers.SerializerMethodField()
    medication_details = rest_serializers.SerializerMethodField()
    patient_timeline = rest_serializers.SerializerMethodField()
    facility_details = rest_serializers.SerializerMethodField()
    patient_lab_details = rest_serializers.SerializerMethodField()

    def get_patient_family_details(self, instance):
        return PatientFamilySerializer(patient_models.PatientFamily.objects.filter(patient=instance), many=True).data

    def get_portie_calling_details(self, instance):
        return PortieCallingDetailSerializer(
            patient_models.PortieCallingDetail.objects.filter(patient=instance), many=True,
        ).data

    def get_contact_details(self, instance):
        return ContactDetailsSerializer(instance).data

    def get_medication_details(self, instance):
        return MedicationDetailsSerializer(patient_models.Patient.objects.filter(id=instance.id), many=True).data

    def get_facility_details(self, instance):
        return PatientFacilityDetailsSerializer(
            facility_models.Facility.objects.filter(id=instance.facility.id), many=True
        ).data

    def get_patient_timeline(self, instance):
        return PatientTimeLineSerializer(
            patient_models.PatientTimeLine.objects.filter(patient=instance), many=True
        ).data

    def get_patient_lab_details(self, instance):
        return PatientLabSerializer(patient_models.PatientSampleTest.objects.filter(patient=instance), many=True).data

    def get_personal_details(self, instance):
        return PersonalDetailsSerializer(patient_models.Patient.objects.filter(id=instance.id), many=True).data

    class Meta:
        model = None
        fields = (
            "personal_details",
            "patient_family_details",
            "portie_calling_details",
            "contact_details",
            "medication_details",
            "facility_details",
            "patient_timeline",
            "patient_lab_details",
        )
