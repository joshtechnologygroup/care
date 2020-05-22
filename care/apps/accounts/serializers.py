from rest_framework.serializers import ModelSerializer

from apps.accounts import models as accounts_models
from django.contrib.auth import password_validation, hashers

class UserInfoUpdateSerializer(ModelSerializer):

    class Meta:
        model = accounts_models.User
        fields = ('first_name','last_name', 'phone_number')
        # extra_kwargs = {
        #     'district': {'write_only': True},
        # }
    def validate(self, attrs):
        print('aaaaa')
        # attrs['manager'] = self.context['request'].user
        return attrs    

class PasswordUpdateSerializer(ModelSerializer):

    class Meta:
        model = accounts_models.User
        fields = ('password',)

    def validate(self, attrs):
        print(attrs,"password")
        password_validation.validate_password(data['password'])
        data['password'] = hashers.make_password(data['password'])
        return attrs          


class UserSerializer(PasswordUpdateSerializer, UserInfoUpdateSerializer):

    class Meta:
        model = accounts_models.User
        fields = ('district','user_type',) + PasswordUpdateSerializer.Meta.fields + UserInfoUpdateSerializer.Meta.fields
        extra_kwargs = {
            'district': {'write_only': True},
            'password': {'write_only': True},
        }

    # def validate(self, attrs):
    #     return super().validate(attrs)
    #     attrs.validate_password
    #     attrs['manager'] = self.context['request'].user
    #     return attrs        

    def update(self, instance, validated_data):
        return super(UserSerializer, self).update(instance, validated_data)
