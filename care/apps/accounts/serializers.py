from rest_framework.serializers import ModelSerializer

from apps.accounts import models as accounts_models
from django.contrib.auth import password_validation, hashers

class UserInfoUpdateSerializer(ModelSerializer):

    class Meta:
        model = accounts_models.User
        fields = ('first_name','last_name', 'phone_number',)


class PasswordUpdateSerializer(ModelSerializer):

    class Meta:
        model = accounts_models.User
        fields = ('password',)
        extra_kwargs = {
            'password': {'write_only': True,'required': True},
        }

    def validate_password(self, password):
        password_validation.validate_password(password)
        password = hashers.make_password(password)
        return password            


class UserSerializer(PasswordUpdateSerializer, UserInfoUpdateSerializer):

    class Meta:
        model = accounts_models.User
        fields = ('district','user_type','email',) + PasswordUpdateSerializer.Meta.fields + UserInfoUpdateSerializer.Meta.fields
        extra_kwargs = {
            'password': {'write_only': False,'required': False},
            'user_type': {'write_only': True}
        }  
