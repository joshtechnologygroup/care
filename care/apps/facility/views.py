from rest_framework.decorators import action
from rest_framework import viewsets, mixins, permissions, filters as rest_filters
from django_filters import rest_framework as filters
from rest_framework.response import Response

from apps.commons import (
    constants as commons_constants,
    pagination as commons_pagination,
)
from apps.facility import (
    models as facility_models,
    serializers as facility_serializers,
    filters as facility_filters,
)


class FacilityViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet for Facility list and create
    """

    queryset = facility_models.Facility.objects.all()
    serializer_class = facility_serializers.FacilitySerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    )
    ordering_fields = (
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
    filterset_class = facility_filters.FacilityFilter
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = commons_pagination.CustomPagination

    def get_queryset(self):
        filter_kwargs = {}
        print(self.request.user.user_type)
        if self.request.user.user_type:
            if self.request.user.user_type.name == commons_constants.FACILITY_USER:
                print('2121')
                filter_kwargs["facilityuser__user"] = self.request.user
            elif self.request.user.user_type.name == commons_constants.PORTEA:
                filter_kwargs["id__in"] = []
        return facility_models.Facility.objects.filter(**filter_kwargs)

    @action(detail=False)
    def short(self, *args, **kwargs):
        return Response(
            facility_serializers.FacilityShortSerializer(
                instance=facility_models.Facility.objects.order_by('name').all(),
                many=True
            ).data
        )


class FacilityUserViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet for FacilityUser add and remove
    """

    queryset = facility_models.FacilityUser.objects.all()
    serializer_class = facility_serializers.FacilityUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class FacilityTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Faciity type list
    """

    queryset = facility_models.FacilityType.objects.all()
    serializer_class = facility_serializers.FacilityTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class InventoryViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for Inventory add, list and update
    """

    queryset = facility_models.Inventory.objects.all()
    filter_backends = (filters.DjangoFilterBackend, rest_filters.OrderingFilter)
    ordering_fields = (
        "facility__name",
        "item__name",
        "required_quantity",
        "current_quantity",
        "updated_at",
    )
    filterset_class = facility_filters.InventoryFilter
    serializer_class = facility_serializers.InventorySerializer
    pagination_class = commons_pagination.CustomPagination
    permission_classes = (permissions.IsAuthenticated,)


class FacilityStaffViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for facility staff add, list and update
    """

    queryset = facility_models.FacilityStaff.objects.all()
    serializer_class = facility_serializers.FacilityStaffSerializer
    pagination_class = commons_pagination.CustomPagination
    permission_classes = (permissions.IsAuthenticated,)


class FacilityInfrastructureViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for facility infrastructure add, list and update
    """

    queryset = facility_models.FacilityInfrastructure.objects.all()
    serializer_class = facility_serializers.FacilityInfrastructureSerializer
    pagination_class = commons_pagination.CustomPagination
    permission_classes = (permissions.IsAuthenticated,)


class InventoryItemViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet,
):
    """
    ViewSet for Inventory Item add, list and update
    """

    queryset = facility_models.InventoryItem.objects.all()
    serializer_class = facility_serializers.InventoryItemSerializer
    pagination_class = commons_pagination.CustomPagination
    permission_classes = (permissions.IsAuthenticated,)
