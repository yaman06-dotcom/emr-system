from django.db import models
from django.conf import settings
from patients.models import Patient


class MedicalVisit(models.Model):
    """
    Medical Visit model to record patient visits
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='visits')
    visit_date = models.DateTimeField(auto_now_add=True)
    
    # Visit Details
    chief_complaint = models.TextField(help_text="Main reason for visit")
    symptoms = models.TextField(help_text="Symptoms reported by patient")
    diagnosis = models.TextField(help_text="Doctor's diagnosis")
    
    # Vital Signs
    blood_pressure_systolic = models.IntegerField(blank=True, null=True, help_text="Systolic BP (mmHg)")
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True, help_text="Diastolic BP (mmHg)")
    heart_rate = models.IntegerField(blank=True, null=True, help_text="Heart rate (bpm)")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="Temperature (°C)")
    respiratory_rate = models.IntegerField(blank=True, null=True, help_text="Respiratory rate (breaths/min)")
    
    # Notes
    doctor_notes = models.TextField(blank=True, null=True, help_text="Additional notes from doctor")
    treatment_plan = models.TextField(blank=True, null=True, help_text="Recommended treatment plan")
    follow_up_date = models.DateField(blank=True, null=True, help_text="Recommended follow-up date")
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_date']
        indexes = [
            models.Index(fields=['patient', '-visit_date']),
            models.Index(fields=['doctor', '-visit_date']),
        ]
    
    def __str__(self):
        return f"Visit: {self.patient.get_full_name()} on {self.visit_date.strftime('%Y-%m-%d %H:%M')}"
    
    def get_blood_pressure(self):
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
        return "N/A"


class Prescription(models.Model):
    """
    Prescription model to manage medications prescribed during visits
    """
    visit = models.ForeignKey(MedicalVisit, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='prescriptions')
    
    # Medication Details
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg, 10ml")
    frequency = models.CharField(max_length=100, help_text="e.g., twice daily, every 8 hours")
    duration = models.CharField(max_length=100, help_text="e.g., 7 days, 2 weeks")
    instructions = models.TextField(blank=True, null=True, help_text="Special instructions for taking medication")
    
    # Alerts
    has_allergy_alert = models.BooleanField(default=False)
    allergy_alert_message = models.TextField(blank=True, null=True)
    has_conflict_alert = models.BooleanField(default=False)
    conflict_alert_message = models.TextField(blank=True, null=True)
    
    # System Fields
    prescribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-prescribed_date']
        indexes = [
            models.Index(fields=['patient', '-prescribed_date']),
            models.Index(fields=['medication_name']),
        ]
    
    def __str__(self):
        return f"{self.medication_name} - {self.patient.get_full_name()}"
    
    def check_allergy_alert(self):
        """
        Check if patient has allergies to the prescribed medication
        """
        if self.patient.allergies:
            allergies_list = [a.strip().lower() for a in self.patient.allergies.split(',')]
            medication_lower = self.medication_name.lower()
            
            for allergy in allergies_list:
                if allergy in medication_lower or medication_lower in allergy:
                    self.has_allergy_alert = True
                    self.allergy_alert_message = f"WARNING: Patient is allergic to {allergy}!"
                    return True
        
        self.has_allergy_alert = False
        self.allergy_alert_message = None
        return False
    
    def check_drug_conflicts(self):
        """
        Check for potential drug conflicts with current medications
        Simple rule-based checking
        """
        # Get active prescriptions for this patient (excluding current one)
        active_prescriptions = Prescription.objects.filter(
            patient=self.patient,
            is_active=True
        ).exclude(id=self.id)
        
        # Simple conflict rules (can be expanded)
        conflict_rules = {
            'warfarin': ['aspirin', 'ibuprofen', 'naproxen'],
            'aspirin': ['warfarin', 'heparin'],
            'metformin': ['alcohol'],
            'insulin': ['alcohol'],
        }
        
        medication_lower = self.medication_name.lower()
        conflicts = []
        
        for prescription in active_prescriptions:
            other_med = prescription.medication_name.lower()
            
            # Check if current medication has conflicts
            for drug, conflicting_drugs in conflict_rules.items():
                if drug in medication_lower:
                    for conflicting in conflicting_drugs:
                        if conflicting in other_med:
                            conflicts.append(f"{prescription.medication_name}")
        
        if conflicts:
            self.has_conflict_alert = True
            self.conflict_alert_message = f"WARNING: Potential conflict with: {', '.join(conflicts)}"
            return True
        
        self.has_conflict_alert = False
        self.conflict_alert_message = None
        return False
    
    def save(self, *args, **kwargs):
        """
        Override save to check for alerts before saving
        """
        self.check_allergy_alert()
        self.check_drug_conflicts()
        super().save(*args, **kwargs)
