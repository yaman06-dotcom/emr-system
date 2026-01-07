from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HealthRiskPrediction
from patients.models import Patient
from .forms import HealthRiskPredictionForm
from .ml_model import predictor


@login_required
def predict_risk(request, patient_id):
    """
    Create a health risk prediction for a patient
    """
    patient = get_object_or_404(Patient, id=patient_id, is_active=True)
    
    if request.method == 'POST':
        form = HealthRiskPredictionForm(request.POST)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.patient = patient
            prediction.predicted_by = request.user
            
            # Get AI prediction
            risk_level, risk_score = predictor.predict(
                age=prediction.age,
                bmi=float(prediction.bmi),
                bp_systolic=prediction.blood_pressure_systolic,
                bp_diastolic=prediction.blood_pressure_diastolic,
                has_family_history=prediction.has_family_history
            )
            
            prediction.risk_level = risk_level
            prediction.risk_score = risk_score
            prediction.recommendations = prediction.get_recommendations()
            prediction.save()
            
            messages.success(request, f'Health risk prediction completed: {risk_level} Risk')
            return redirect('prediction_detail', prediction_id=prediction.id)
    else:
        # Pre-fill form with patient data if available
        initial_data = {
            'age': patient.get_age(),
            'bmi': patient.calculate_bmi(),
        }
        
        # Get latest visit for blood pressure data
        latest_visit = patient.visits.first()
        if latest_visit:
            initial_data['blood_pressure_systolic'] = latest_visit.blood_pressure_systolic
            initial_data['blood_pressure_diastolic'] = latest_visit.blood_pressure_diastolic
        
        # Check family history
        if patient.family_history and 'diabetes' in patient.family_history.lower():
            initial_data['has_family_history'] = True
        
        form = HealthRiskPredictionForm(initial=initial_data)
    
    return render(request, 'ai_prediction/prediction_form.html', {
        'form': form,
        'patient': patient,
    })


@login_required
def prediction_detail(request, prediction_id):
    """
    View detailed information about a health risk prediction
    """
    prediction = get_object_or_404(HealthRiskPrediction, id=prediction_id)
    
    context = {
        'prediction': prediction,
    }
    return render(request, 'ai_prediction/prediction_detail.html', context)


@login_required
def prediction_list(request):
    """
    List all health risk predictions
    """
    predictions = HealthRiskPrediction.objects.all()
    
    context = {
        'predictions': predictions,
    }
    return render(request, 'ai_prediction/prediction_list.html', context)


@login_required
def train_model_view(request):
    """
    Admin view to train/retrain the ML model
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to train the model.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            predictor.train_model()
            messages.success(request, 'Model has been trained successfully!')
        except Exception as e:
            messages.error(request, f'Error training model: {str(e)}')
        return redirect('dashboard')
    
    return render(request, 'ai_prediction/train_model.html')
