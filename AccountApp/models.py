from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


validate_eight_digits = RegexValidator(r"^\d{8}$", "Saisissez exactement huit chiffres.")


def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("La date de naissance doit être antérieure à aujourd’hui.")


class User(AbstractUser):
    pass


class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(User):
    license_number = models.CharField(
        max_length=6, unique=True, validators=[MinLengthValidator(6)]
    )
    phone = models.CharField(max_length=8, validators=[validate_eight_digits])
    specialties = models.ManyToManyField(Specialty, related_name="doctors")


class Patient(User):
    national_id = models.CharField(
        max_length=8, unique=True, validators=[validate_eight_digits]
    )
    phone = models.CharField(max_length=8, validators=[validate_eight_digits])
    birth_date = models.DateField(validators=[validate_past_date])
