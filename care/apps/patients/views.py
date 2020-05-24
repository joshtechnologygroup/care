from django_filters import rest_framework as filters
from rest_framework import (
    mixins as rest_mixins,
    viewsets as rest_viewsets,
)

from apps.patients import (
    filters as patients_filters,
    models as patients_models,
    serializers as patients_serializers,
)


class PatientTimeLineViewSet(rest_mixins.ListModelMixin, rest_viewsets.GenericViewSet):
    """
    ViewSet for Patient Timeline List
    """

    serializer_class = patients_serializers.PatientTimeLineSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = patients_filters.PatientTimelineFilter

    def get_queryset(self):
        return patients_models.PatientTimeLine.objects.filter(
            patient__id=self.kwargs.get("patient_id")
        )
