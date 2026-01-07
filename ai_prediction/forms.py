from django import forms
from .models import HealthRiskPrediction


class HealthRiskPredictionForm(forms.ModelForm):
    """
    Form for creating health risk predictions
    """
    class Meta:
        model = HealthRiskPrediction
        fields = ['age', 'bmi', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'has_family_history', 'notes']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age in years'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'BMI'}),
            'blood_pressure_systolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Systolic BP (mmHg)'}),
            'blood_pressure_diastolic': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Diastolic BP (mmHg)'}),
            'has_family_history': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
