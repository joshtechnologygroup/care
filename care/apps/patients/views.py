from django.db.models import F

from django_filters import rest_framework as filters

from rest_framework import (
    filters as rest_filters,
    generics as rest_generics,
    mixins as rest_mixins,
    permissions as rest_permissions,
    status as rest_status,
    viewsets as rest_viewsets,
)
from rest_framework.response import Response
from rest_framework import status
from apps.commons import (
    constants as commons_constants,
    filters as commons_filters,
    pagination as commons_pagination,
)
from apps.patients import (
    constants as patients_constants,
    models as patient_models,
    serializers as patient_serializers,
    filters as patients_filters,
)
from apps.facility import models as facility_models


class PatientViewSet(rest_viewsets.ModelViewSet):

    serializer_class = patient_serializers.PatientSerializer
    pagination_class = commons_pagination.CustomPagination
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    )
    filterset_class = patients_filters.PatientFilter
    permission_classes = (rest_permissions.IsAuthenticated,)
    ordering_fields = (
        "name",
        "icmr_id",
        "govt_id",
        "facility",
        "year",
    )

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = patient_serializers.PatientDetailsSerializer
        return super().retrieve(request, *args, **kwargs)

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly." % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = queryset.filter(**filter_kwargs).first()

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        queryset = patient_models.Patient.objects.all()
        if self.request.user.user_type and self.request.user.user_type.name == commons_constants.PORTEA:
            queryset = queryset.filter(patient_status=patients_constants.HOME_ISOLATION)
        elif self.request.user.user_type and self.request.user.user_type.name == commons_constants.FACILITY_MANAGER:
            facility_ids = list(
                facility_models.FacilityUser.objects.filter(user_id=self.request.user.id).values_list(
                    "facility_id", flat=True
                )
            )
            queryset = queryset.filter(patientfacility__facility_id__in=facility_ids)
        queryset = queryset.annotate(
            facility_status=F("patientfacility__patient_status__name"),
            facility_name=F("patientfacility__facility__name"),
            facility_type=F("patientfacility__facility__facility_type__name"),
            ownership_type=F("patientfacility__facility__owned_by__name"),
            facility_district=F("patientfacility__facility__district__name"),
        )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(patient_serializers.PatientDetailsSerializer(instance).data, status=status.HTTP_201_CREATED)


class PatientGroupViewSet(rest_viewsets.ModelViewSet):

    queryset = patient_models.PatientGroup.objects.all()
    serializer_class = patient_serializers.PatientGroupSerializer


class CovidStatusViewSet(rest_viewsets.ModelViewSet):

    queryset = patient_models.CovidStatus.objects.all()
    serializer_class = patient_serializers.CovidStatusSerializer


class ClinicalStatusViewSet(rest_viewsets.ModelViewSet):

    queryset = patient_models.ClinicalStatus.objects.all()
    serializer_class = patient_serializers.ClinicalStatusSerializer


class PatientStatusViewSet(rest_viewsets.ModelViewSet):

    queryset = patient_models.PatientStatus.objects.all()
    serializer_class = patient_serializers.PatientStatusSerializer


class PatientTimeLineViewSet(rest_mixins.ListModelMixin, rest_viewsets.GenericViewSet):
    """
    ViewSet for Patient Timeline List
    """

    serializer_class = patient_serializers.PatientTimeLineSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = patients_filters.PatientTimelineFilter
    pagination_class = commons_pagination.CustomPagination
    permission_classes = (rest_permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = patient_models.PatientTimeLine.objects.filter(patient_id=self.kwargs.get("patient_id"))
        if self.request.user.user_type and self.request.user.user_type.name == commons_constants.PORTEA:
            queryset = queryset.filter(patient__patient_status=patients_constants.HOME_ISOLATION)
        elif self.request.user.user_type and self.request.user.user_type.name == commons_constants.FACILITY_MANAGER:
            facility_ids = list(
                facility_models.FacilityUser.objects.filter(user_id=self.request.user.id).values_list(
                    "facility_id", flat=True
                )
            )
            queryset = queryset.filter(patient__patientfacility__facility_id__in=facility_ids)
        return queryset


class PortieCallingDetailViewSet(
    rest_mixins.CreateModelMixin, rest_mixins.UpdateModelMixin, rest_viewsets.GenericViewSet,
):
    """
    views for create and update portie calling detail
    """

    serializer_class = patient_serializers.PortieCallingDetailSerialzier
    permission_classes = (rest_permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = patient_models.PortieCallingDetail.objects.all()
        if self.request.user.user_type and self.request.user.user_type.name == commons_constants.FACILITY_MANAGER:
            facility_ids = list(
                facility_models.FacilityUser.objects.filter(user_id=self.request.user.id).values_list(
                    "facility_id", flat=True
                )
            )
            queryset = queryset.filter(patient__patientfacility__facility_id__in=facility_ids)
        return queryset


class PatientSampleTestViewSet(
    rest_mixins.CreateModelMixin, rest_mixins.UpdateModelMixin, rest_viewsets.GenericViewSet,
):
    """
    views for create and update patient sample test
    """

    queryset = patient_models.PatientSampleTest.objects.all()
    serializer_class = patient_serializers.PatientSampleTestSerializer
    permission_classes = (rest_permissions.IsAuthenticated,)


class PatientTransferViewSet(
    rest_mixins.ListModelMixin, rest_mixins.UpdateModelMixin, rest_viewsets.GenericViewSet,
):
    """
    ViewSet for Patient Transfer List
    """

    http_method_names = ("patch", "get")
    queryset = patient_models.PatientTransfer.objects.all()
    serializer_class = patient_serializers.PatientTransferSerializer
    permission_classes = (rest_permissions.IsAuthenticated,)
    pagination_class = commons_pagination.CustomPagination
    filter_backends = (
        filters.DjangoFilterBackend,
        commons_filters.ReplaceFieldsOrderingFilter,
        rest_filters.SearchFilter,
    )
    filterset_class = patients_filters.PatientTransferFilter
    search_fields = (
        "^from_patient_facility__patient__icmr_id",
        "^from_patient_facility__patient__govt_id",
        "^from_patient_facility__patient__name",
        "^from_patient_facility__patient__phone_number",
        "^from_patient_facility__facility__facility_code",
        "^to_facility__facility_code",
    )
    ordering_fields = (
        "icmr_id",
        "govt_id",
        "patient_name",
        "month",
        "year",
        "phone_number",
        "requested_at",
        "status_updated_at",
        "from_facility_id",
        "to_facility_id",
    )
    related_ordering_fields_map = {
        "icmr_id": "from_patient_facility__patient__icmr_id",
        "govt_id": "from_patient_facility__patient__govt_id",
        "patient_name": "from_patient_facility__patient__name",
        "month": "from_patient_facility__patient__month",
        "year": "from_patient_facility__patient__year",
        "phone_number": "from_patient_facility__patient__phone_number",
        "from_facility_id": "from_patient_facility__facility_id",
        "requested_at": "created_at",
    }

    def get_serializer_class(self):
        if self.action == "partial_update":
            return patient_serializers.PatientTransferUpdateSerializer
        return self.serializer_class


class PatientFamilyViewSet(
    rest_mixins.CreateModelMixin, rest_mixins.UpdateModelMixin, rest_viewsets.GenericViewSet,
):
    """
    views for create and update patient family member
    """

    queryset = patient_models.PatientFamily.objects.all()
    serializer_class = patient_serializers.PatientFamilySerializer
    permission_classes = (rest_permissions.IsAuthenticated,)
    pagination_class = None
