from django import forms
from .models import MedicalVisit, Prescription
from patients.models import Patient


class MedicalVisitForm(forms.ModelForm):
    """
    Form for creating and updating medical visits
    """
    class Meta:
        model = MedicalVisit
        fields = [
            'patient', 'chief_complaint', 'symptoms', 'diagnosis',
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'temperature', 'respiratory_rate',
            'doctor_notes', 'treatment_plan', 'follow_up_date'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'chief_complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'blood_pressure_systolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Systolic (mmHg)'}),
            'blood_pressure_diastolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Diastolic (mmHg)'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Heart rate (bpm)'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Temperature (°C)'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Breaths/min'}),
            'doctor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PrescriptionForm(forms.ModelForm):
    """
    Form for creating prescriptions
    """
    class Meta:
        model = Prescription
        fields = [
            'medication_name', 'dosage', 'frequency', 'duration', 'instructions'
        ]
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., twice daily'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 7 days'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
