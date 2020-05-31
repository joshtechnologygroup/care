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
