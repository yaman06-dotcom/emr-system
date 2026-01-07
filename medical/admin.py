from django.contrib import admin
from .models import MedicalVisit, Prescription


@admin.register(MedicalVisit)
class MedicalVisitAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'visit_date', 'diagnosis']
    list_filter = ['visit_date', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medication_name', 'patient', 'doctor', 'prescribed_date', 'is_active', 'has_allergy_alert', 'has_conflict_alert']
    list_filter = ['is_active', 'has_allergy_alert', 'has_conflict_alert', 'prescribed_date']
    search_fields = ['medication_name', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['prescribed_date', 'has_allergy_alert', 'allergy_alert_message', 'has_conflict_alert', 'conflict_alert_message']
