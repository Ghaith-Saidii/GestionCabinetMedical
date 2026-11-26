from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models, router
from django.utils import timezone


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    doctor = models.ForeignKey("AccountApp.Doctor", on_delete=models.PROTECT)
    patient = models.ForeignKey("AccountApp.Patient", on_delete=models.PROTECT)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    prescription = models.FileField(
        upload_to="prescriptions/",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
    )
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.PENDING)
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
            ),
        ]

    def clean(self):
        super().clean()
        if not isinstance(self.appointment_date, datetime):
            return

        appointment_date = self.appointment_date
        if timezone.is_naive(appointment_date):
            appointment_date = timezone.make_aware(appointment_date)
        if appointment_date > timezone.now():
            return

        if not self._state.adding:
            database = router.db_for_write(type(self), instance=self)
            unchanged = type(self).objects.using(database).filter(
                pk=self.pk, appointment_date=appointment_date
            ).exists()
            if unchanged:
                return

        raise ValidationError({
            "appointment_date": "La date du rendez-vous doit être dans le futur."
        })
