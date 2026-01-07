from django.contrib import admin
from .models import HealthRiskPrediction


@admin.register(HealthRiskPrediction)
class HealthRiskPredictionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'risk_level', 'risk_score', 'prediction_date', 'predicted_by']
    list_filter = ['risk_level', 'prediction_date', 'has_family_history']
    search_fields = ['patient__first_name', 'patient__last_name']
    readonly_fields = ['prediction_date', 'risk_level', 'risk_score', 'recommendations']
