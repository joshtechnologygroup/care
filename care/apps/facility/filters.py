from django.db import models as django_models
import django_filters
from django_filters import rest_framework as filters

from apps.accounts import models as accounts_models
from apps.facility import models as facility_models


class FacilityFilter(filters.FilterSet):
    district = filters.filters.ModelMultipleChoiceFilter(
        field_name="district", queryset=accounts_models.District.objects.all()
    )

    class Meta:
        model = facility_models.Facility
        fields = {
            "positive_patient": ["exact", "range", "gt", "lt"],
            "negative_patient": ["exact", "range", "gt", "lt"],
            "total_patient": ["exact", "range", "gt", "lt"],
            "district": ["exact"],
        }


class InventoryFilter(filters.FilterSet):
    item = filters.CharFilter(field_name="item__name")
    facility = filters.CharFilter(field_name="facility__name", lookup_expr="istartswith")
    updated_at = filters.IsoDateTimeFilter()

    class Meta:
        model = facility_models.Inventory
        fields = {
            "current_quantity": ["exact", "range", "gt", "lt"],
            "required_quantity": ["exact", "range", "gt", "lt"],
        }


class FacilityInfrastructureFilter(filters.FilterSet):
    facility = filters.ModelMultipleChoiceFilter(queryset=facility_models.Facility.objects.all())
    room_type = filters.ModelMultipleChoiceFilter(queryset=facility_models.RoomType.objects.all())
    bed_type = filters.ModelMultipleChoiceFilter(queryset=facility_models.BedType.objects.all())
    total_bed = filters.RangeFilter(field_name="total_bed", lookup_expr="range")
    occupied_bed = filters.RangeFilter(field_name="occupied_bed", lookup_expr="range")
    available_bed = filters.RangeFilter(field_name="available_bed", lookup_expr="range")

    class Meta:
        model = facility_models.FacilityInfrastructure
        fields = (
            "facility",
            "room_type",
            "bed_type",
            "total_bed",
            "occupied_bed",
            "available_bed",
        )


class FacilityStaffFilter(filters.FilterSet):
    facility = filters.ModelMultipleChoiceFilter(queryset=facility_models.Facility.objects.all())
    name = filters.CharFilter(lookup_expr='istartswith')
    phone_number = filters.CharFilter()
    email = filters.CharFilter()
    designation = filters.ModelMultipleChoiceFilter(
        field_name="designation__name",
        queryset=facility_models.StaffDesignation.objects.all()
    )

    class Meta:
        model = facility_models.FacilityStaff
        fields = ("facility", "name", "phone_number", "email", "designation")
