from django.utils.translation import ugettext as _

from rest_framework import serializers as rest_serializers
from rest_framework.authtoken.models import Token

from apps.accounts import models as accounts_models
from django.contrib.auth import password_validation, hashers

class UserSerializer(rest_serializers.ModelSerializer):

    def validate_password(self, password):
        password_validation.validate_password(password)
        password = hashers.make_password(password)
        return password

    class Meta:
        model = accounts_models.User
        fields = ('district', 'user_type', 'email','first_name', 'last_name', 'phone_number','password',)
        extra_kwargs = {
            'password': {'write_only':True, 'required': False},
            'user_type': {'write_only': True}
        }


class StateSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for state model
    """
    class Meta:
        model = accounts_models.State
        fields = ('id', 'name',)


class DistrictSerializer(rest_serializers.ModelSerializer):
    """
    Serializer for state model
    """
    class Meta:
        model = accounts_models.District
        fields = ('id', 'name',)


class LoginSerializer(rest_serializers.Serializer):
    """
    User login serializer
    """
    email = rest_serializers.CharField(label=_('Email'))
    password = rest_serializers.CharField(label=_('Password'), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = accounts_models.User.objects.filter(email=email).first()
            if not user or not user.check_password(password):
                msg = _('Your Email or Password is incorrect.Please try again, or click Forgot Password.')
                raise rest_serializers.ValidationError(msg)
        else:
            msg = _('Email/Password parameter is missing or invalid.')
            raise rest_serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class LoginResponseSerializer(rest_serializers.ModelSerializer):
    """
    User login response serializer
    """
    token = rest_serializers.SerializerMethodField()

    class Meta:
        model = accounts_models.User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'token', 'local_body',
        )

    def get_token(self, instance):
        token, _ = Token.objects.get_or_create(user=instance)
        return token.key


class LocalBodySerializer(rest_serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = accounts_models.LocalBody
        fields = (
            'district', 'name', 'body_type', 'localbody_code'
        )
