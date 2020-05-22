from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from apps.accounts import (
    models as accounts_models,
    serializers as accounts_serializers
)


class UserViewSet(ModelViewSet):

    queryset = accounts_models.User.objects.all()
    serializer_class = accounts_serializers.UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return accounts_models.objects.filter(user=self.request.user)

