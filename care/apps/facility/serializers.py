from django.utils.translation import ugettext as _

from rest_framework import serializers as rest_serializers

from apps.commons import constants as commons_constants
from apps.facility import models as facility_models


class FacilityShortSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.Facility
        fields = (
            "id",
            "name",
        )


class FacilitySerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.Facility
        fields = (
            "id",
            "name",
            "facility_code",
            "facility_type",
            "location",
            "address",
            "local_body",
            "district",
            "state",
            "phone_number",
            "corona_testing",
            "created_by",
            "owned_by",
            "total_patient",
            "positive_patient",
            "negative_patient",
        )


class FacilityUserSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.FacilityUser
        fields = (
            "facility",
            "user",
            "created_by",
        )

    def validate(self, attrs):
        current_user = self.context['request'].user
        if current_user.user_type and current_user.user_type.name == commons_constants.FACILITY_MANAGER:
            if not current_user.facilityuser_set.filter(facility=attrs['facility']).exists():
                raise rest_serializers.ValidationError(
                    _("You do not have permission to perform this action.")
                )
        elif current_user.user_type and current_user.user_type.name == commons_constants.PORTEA:
            raise rest_serializers.ValidationError(
                _("You do not have permission to perform this action.")
            )
        return attrs


class FacilityTypeSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.FacilityType
        fields = (
            "id",
            "name",
        )


class FacilityStaffSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.FacilityStaff
        fields = (
            "id",
            "facility",
            "name",
            "phone_number",
            "email",
            "designation",
        )

    def validate(self, attrs):
        current_user = self.context['request'].user
        if current_user.user_type and current_user.user_type.name == commons_constants.FACILITY_MANAGER:
            if not current_user.facilityuser_set.filter(facility=attrs['facility']).exists():
                raise rest_serializers.ValidationError(
                    _("You do not have permission to perform this action.")
                )
        elif current_user.user_type and current_user.user_type.name == commons_constants.PORTEA:
            raise rest_serializers.ValidationError(
                _("You do not have permission to perform this action.")
            )
        return attrs


class FacilityInfrastructureSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.FacilityInfrastructure
        fields = ("facility", "room_type", "bed_type", "total_bed", "occupied_bed", "available_bed", "updated_at")


    def validate(self, attrs):
        current_user = self.context['request'].user
        if current_user.user_type and current_user.user_type.name == commons_constants.FACILITY_MANAGER:
            if not current_user.facilityuser_set.filter(facility=attrs['facility']).exists():
                raise rest_serializers.ValidationError(
                    _("You do not have permission to perform this action.")
                )
        elif current_user.user_type and current_user.user_type.name == commons_constants.PORTEA:
            raise rest_serializers.ValidationError(
                _("You do not have permission to perform this action.")
            )
        return attrs


class FacilityInfrastructureUpdateSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.FacilityInfrastructure
        fields = (
            "total_bed",
            "occupied_bed",
            "available_bed",
        )

    def validate(self, attrs):
        current_user = self.context['request'].user
        if current_user.user_type and current_user.user_type.name == commons_constants.FACILITY_MANAGER:
            if not current_user.facilityuser_set.filter(facility=self.instance.facility).exists():
                raise rest_serializers.ValidationError(
                    _("You do not have permission to perform this action.")
                )
        elif current_user.user_type and current_user.user_type.name == commons_constants.PORTEA:
            raise rest_serializers.ValidationError(
                _("You do not have permission to perform this action.")
            )
        return attrs


class InventorySerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.Inventory
        fields = (
            "id",
            "facility",
            "item",
            "required_quantity",
            "current_quantity",
            "updated_at",
        )
        extra_kwargs = {
            "required_quantity": {"required": True},
            "current_quantity": {"required": True},
            "updated_at": {"read_only": True},
        }
        validators = [
            rest_serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=("facility", "item"),
                message=_("This Inventory have already added, Update existing one."),
            )
        ]

    def validate(self, attrs):
        attrs["updated_by"] = self.context["request"].user
        return super(InventorySerializer, self).validate(attrs)


class InventoryUpdateSerializer(InventorySerializer):
    class Meta(InventorySerializer.Meta):
        fields = (
            "id",
            "required_quantity",
            "current_quantity",
        )

        validators = ()


class InventoryItemSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.InventoryItem
        fields = (
            "id",
            "name",
        )


class RoomTypeSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.RoomType
        fields = ("id", "name", "description")


class BedTypeSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.RoomType
        fields = ("id", "name", "description")


class StaffDesignationSerializer(rest_serializers.ModelSerializer):
    class Meta:
        model = facility_models.StaffDesignation
        fields = (
            "id",
            "name",
        )
