from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Admin configuration for Patient model
    """
    list_display = ['national_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'is_active']
    list_filter = ['gender', 'blood_type', 'is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'national_id', 'phone_number', 'email']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'national_id', 
                      'phone_number', 'email', 'address')
        }),
        ('Medical Information', {
            'fields': ('blood_type', 'allergies', 'chronic_conditions', 'family_history')
        }),
        ('Health Metrics', {
            'fields': ('height', 'weight')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_active')
        }),
    )
