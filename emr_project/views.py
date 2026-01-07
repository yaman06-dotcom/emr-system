from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from patients.models import Patient
from medical.models import MedicalVisit, Prescription
from ai_prediction.models import HealthRiskPrediction


@login_required
def dashboard(request):
    """
    Main dashboard view with statistics and recent activity
    """
    # Get statistics
    total_patients = Patient.objects.filter(is_active=True).count()
    total_visits = MedicalVisit.objects.count()
    total_prescriptions = Prescription.objects.filter(is_active=True).count()
    
    # Recent visits (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_visits_count = MedicalVisit.objects.filter(visit_date__gte=seven_days_ago).count()
    
    # Risk predictions statistics
    risk_stats = HealthRiskPrediction.objects.values('risk_level').annotate(count=Count('id'))
    risk_distribution = {item['risk_level']: item['count'] for item in risk_stats}
    
    # Recent visits
    recent_visits = MedicalVisit.objects.select_related('patient', 'doctor').all()[:10]
    
    # Recent patients
    recent_patients = Patient.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Prescription alerts
    allergy_alerts = Prescription.objects.filter(has_allergy_alert=True, is_active=True).count()
    conflict_alerts = Prescription.objects.filter(has_conflict_alert=True, is_active=True).count()
    
    # High risk patients
    high_risk_predictions = HealthRiskPrediction.objects.filter(
        risk_level='HIGH'
    ).select_related('patient').order_by('-prediction_date')[:5]
    
    context = {
        'total_patients': total_patients,
        'total_visits': total_visits,
        'total_prescriptions': total_prescriptions,
        'recent_visits_count': recent_visits_count,
        'risk_distribution': risk_distribution,
        'recent_visits': recent_visits,
        'recent_patients': recent_patients,
        'allergy_alerts': allergy_alerts,
        'conflict_alerts': conflict_alerts,
        'high_risk_predictions': high_risk_predictions,
    }
    
    return render(request, 'dashboard.html', context)
