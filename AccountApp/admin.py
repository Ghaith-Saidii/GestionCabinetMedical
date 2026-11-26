from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Doctor, Patient, Specialty, User


admin.site.register(User, UserAdmin)
admin.site.register(Specialty)


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Médecin", {"fields": ("license_number", "phone", "specialties")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Médecin", {"fields": ("license_number", "phone", "specialties")}),
    )

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        return (*fields, "license_number") if obj is not None else fields


@admin.register(Patient)
class PatientAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Patient", {"fields": ("national_id", "phone", "birth_date")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Patient", {"fields": ("national_id", "phone", "birth_date")}),
    )

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        return (*fields, "national_id") if obj is not None else fields
