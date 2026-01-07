from django.db import models
from django.conf import settings
from patients.models import Patient


class HealthRiskPrediction(models.Model):
    """
    Model to store AI-based health risk predictions
    Predicts diabetes risk based on patient health metrics
    """
    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='risk_predictions')
    predicted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='predictions')
    
    # Input Features
    age = models.IntegerField()
    bmi = models.DecimalField(max_digits=5, decimal_places=2)
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    has_family_history = models.BooleanField(default=False, help_text="Family history of diabetes")
    
    # Prediction Results
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    risk_score = models.DecimalField(max_digits=5, decimal_places=4, help_text="Probability score (0-1)")
    
    # Additional Information
    recommendations = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # System Fields
    prediction_date = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, default='1.0')
    
    class Meta:
        ordering = ['-prediction_date']
        indexes = [
            models.Index(fields=['patient', '-prediction_date']),
            models.Index(fields=['risk_level']),
        ]
    
    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.get_risk_level_display()} ({self.prediction_date.strftime('%Y-%m-%d')})"
    
    def get_recommendations(self):
        """
        Generate recommendations based on risk level
        """
        if self.risk_level == 'HIGH':
            return """
            HIGH RISK RECOMMENDATIONS:
            - Schedule immediate consultation with endocrinologist
            - Regular blood glucose monitoring (fasting and post-meal)
            - Adopt low-carb, high-fiber diet
            - Engage in at least 150 minutes of moderate exercise per week
            - Weight management program
            - Regular follow-up every 3 months
            """
        elif self.risk_level == 'MEDIUM':
            return """
            MEDIUM RISK RECOMMENDATIONS:
            - Annual diabetes screening
            - Maintain healthy diet with reduced sugar intake
            - Regular physical activity (at least 30 minutes daily)
            - Monitor weight and BMI
            - Follow-up every 6 months
            """
        else:
            return """
            LOW RISK RECOMMENDATIONS:
            - Continue healthy lifestyle habits
            - Annual health check-up
            - Maintain balanced diet and regular exercise
            - Monitor any changes in health status
            """
