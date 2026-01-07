from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient
from .forms import PatientForm, PatientSearchForm


@login_required
def patient_list(request):
    """
    View to list all patients with search functionality
    """
    search_form = PatientSearchForm(request.GET)
    patients = Patient.objects.filter(is_active=True)
    
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        if search_query:
            patients = patients.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(national_id__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
    
    context = {
        'patients': patients,
        'search_form': search_form,
    }
    return render(request, 'patients/patient_list.html', context)


@login_required
def patient_detail(request, patient_id):
    """
    View to display detailed patient information
    """
    patient = get_object_or_404(Patient, id=patient_id, is_active=True)
    
    # Get related data
    visits = patient.visits.all()[:10]  # Last 10 visits
    prescriptions = patient.prescriptions.filter(is_active=True)[:10]
    risk_predictions = patient.risk_predictions.all()[:5]
    
    context = {
        'patient': patient,
        'visits': visits,
        'prescriptions': prescriptions,
        'risk_predictions': risk_predictions,
        'bmi': patient.calculate_bmi(),
        'age': patient.get_age(),
    }
    return render(request, 'patients/patient_detail.html', context)


@login_required
def patient_create(request):
    """
    View to create a new patient
    """
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(request, f'Patient {patient.get_full_name()} has been created successfully!')
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm()
    
    return render(request, 'patients/patient_form.html', {'form': form, 'action': 'Create'})


@login_required
def patient_update(request, patient_id):
    """
    View to update patient information
    """
    patient = get_object_or_404(Patient, id=patient_id, is_active=True)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient {patient.get_full_name()} has been updated successfully!')
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/patient_form.html', {
        'form': form,
        'patient': patient,
        'action': 'Update'
    })


@login_required
def patient_delete(request, patient_id):
    """
    View to soft delete a patient (set is_active to False)
    """
    patient = get_object_or_404(Patient, id=patient_id, is_active=True)
    
    if request.method == 'POST':
        patient.is_active = False
        patient.save()
        messages.success(request, f'Patient {patient.get_full_name()} has been deleted successfully!')
        return redirect('patient_list')
    
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
