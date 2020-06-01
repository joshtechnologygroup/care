from rest_framework import permissions as rest_permissions

from apps.commons import constants as commons_constants

class AnonymousPermission(rest_permissions.BasePermission):
    """
    Don't Allows access to authenticated users.
    """

    def has_permission(self, request, view):
        return not (request.user and request.user.is_authenticated)


class FacilityAccessPermission(rest_permissions.BasePermission):
    """
    Don't Allows access to portea user
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type and request.user.user_type.name in [
            commons_constants.FACILITY_MANAGER,
            commons_constants.DISTRICT_MANAGER
        ]
