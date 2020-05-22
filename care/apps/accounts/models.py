from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from simple_history.models import HistoricalRecords

from apps.accounts import constants as accounts_constants
from apps.commons import (
    constants as commons_constants,
    models as commons_models,
    validators as commons_validators,
)


class State(commons_models.SoftDeleteTimeStampedModel):
    """
    Model to store States
    """
    name = models.CharField(max_length=commons_constants.FIELDS_CHARACTER_LIMITS['NAME'], help_text='Name of the State')

    def __str__(self):
        return f'{self.name}'


class District(commons_models.SoftDeleteTimeStampedModel):
    """
    Model to store districts
    """
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    name = models.CharField(
        max_length=commons_constants.FIELDS_CHARACTER_LIMITS['NAME'], help_text='Name of the District'
    )

    def __str__(self):
        return f'{self.name}'


class LocalBody(commons_models.SoftDeleteTimeStampedModel):
    """
    Model to store details of local bodies
    """

    district = models.ForeignKey(District, on_delete=models.PROTECT)
    name = models.CharField(
        max_length=commons_constants.FIELDS_CHARACTER_LIMITS['NAME'], help_text='Name of the Local Body'
    )
    body_type = models.PositiveIntegerField(
        choices=accounts_constants.LOCAL_BODY_CHOICES, help_text='denotes the type of local body'
    )
    localbody_code = models.CharField(
        max_length=commons_constants.FIELDS_CHARACTER_LIMITS['LOCALBODY_CODE'],
        blank=True, help_text='Code of local body'
    )

    class Meta:
        unique_together = ('district', 'body_type', 'name',)

    def __str__(self):
        return f'{self.name} ({self.body_type})'


class Skill(commons_models.SoftDeleteTimeStampedModel):
    """
    Model to store skills of auser
    """
    name = models.CharField(max_length=commons_constants.FIELDS_CHARACTER_LIMITS['NAME'], help_text='Name of the skill')
    description = models.TextField(help_text='description of skill')

    def __str__(self):
        return self.name


class CustomUserManager(UserManager):
    """
    Customer object manager for users
    """
    def get_queryset(self):
        return commons_models.SoftDeleteQuerySet(self.model, using=self._db).filter(active=True)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class UserType(commons_models.SoftDeleteTimeStampedModel):
    """
    Model to stores the types of user
    """
    name = models.CharField(max_length=commons_constants.FIELDS_CHARACTER_LIMITS['NAME'], help_text='Type of User')

    def __str__(self):
        return self.name


class User(AbstractUser, commons_models.SoftDeleteTimeStampedModel):
    """
    Model to represent a user
    """
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)
    local_body = models.ForeignKey(LocalBody, on_delete=models.PROTECT, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=True, blank=True)
    phone_number = models.CharField(
        max_length=commons_constants.FIELDS_CHARACTER_LIMITS['PHONE_NUMBER'],
        validators=[commons_validators.phone_number_regex]
    )
    gender = models.IntegerField(choices=commons_constants.GENDER_CHOICES, blank=False)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)
    history = HistoricalRecords()

    REQUIRED_FIELDS = ['email', 'phone_number', 'age', 'gender']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """
        While saving, if the local body is not null, then district will be local body's district
        Overriding save will help in a collision where the local body's district and district fields are different.
        """
        if self.local_body is not None:
            self.district = self.local_body.district
        if self.district is not None:
            self.state = self.district.state
        super().save(*args, **kwargs)