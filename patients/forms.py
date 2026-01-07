from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    """
    Form for creating and updating patient records
    """
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender', 'national_id',
            'phone_number', 'email', 'address', 'blood_type', 'allergies',
            'chronic_conditions', 'family_history', 'height', 'weight'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'List allergies separated by commas'}),
            'chronic_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'family_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height in cm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in kg'}),
        }


class PatientSearchForm(forms.Form):
    """
    Form for searching patients
    """
    search_query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, national ID, or phone number'
        })
    )
