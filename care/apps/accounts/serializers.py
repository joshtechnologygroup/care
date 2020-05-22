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

    def validate(self, attrs):
        password_validation.validate_password(attrs['password'])
        attrs['password'] = hashers.make_password(attrs['password'])
        return super(PasswordUpdateSerializer, self).validate(attrs)          


class UserSerializer(PasswordUpdateSerializer, UserInfoUpdateSerializer):

    class Meta:
        model = accounts_models.User
        fields = ('district','user_type','email',) + PasswordUpdateSerializer.Meta.fields + UserInfoUpdateSerializer.Meta.fields
        extra_kwargs = {
            'password': {'write_only': True},
            'user_type': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs.get('password') is None:
            return super(UserInfoUpdateSerializer, self).validate(attrs)
        return super().validate(attrs)    
