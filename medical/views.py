from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MedicalVisit, Prescription
from patients.models import Patient
from .forms import MedicalVisitForm, PrescriptionForm


@login_required
def visit_create(request, patient_id=None):
    """
    Create a new medical visit
    """
    patient = None
    if patient_id:
        patient = get_object_or_404(Patient, id=patient_id, is_active=True)
    
    if request.method == 'POST':
        form = MedicalVisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.doctor = request.user
            visit.save()
            messages.success(request, 'Medical visit has been recorded successfully!')
            return redirect('visit_detail', visit_id=visit.id)
    else:
        initial_data = {}
        if patient:
            initial_data['patient'] = patient
        form = MedicalVisitForm(initial=initial_data)
    
    return render(request, 'medical/visit_form.html', {
        'form': form,
        'patient': patient,
        'action': 'Create'
    })


@login_required
def visit_detail(request, visit_id):
    """
    View detailed information about a medical visit
    """
    visit = get_object_or_404(MedicalVisit, id=visit_id)
    prescriptions = visit.prescriptions.all()
    
    context = {
        'visit': visit,
        'prescriptions': prescriptions,
    }
    return render(request, 'medical/visit_detail.html', context)


@login_required
def visit_update(request, visit_id):
    """
    Update a medical visit
    """
    visit = get_object_or_404(MedicalVisit, id=visit_id)
    
    if request.method == 'POST':
        form = MedicalVisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical visit has been updated successfully!')
            return redirect('visit_detail', visit_id=visit.id)
    else:
        form = MedicalVisitForm(instance=visit)
    
    return render(request, 'medical/visit_form.html', {
        'form': form,
        'visit': visit,
        'action': 'Update'
    })


@login_required
def visit_list(request):
    """
    List all medical visits
    """
    visits = MedicalVisit.objects.all()
    return render(request, 'medical/visit_list.html', {'visits': visits})


@login_required
def prescription_create(request, visit_id):
    """
    Create a new prescription for a visit
    """
    visit = get_object_or_404(MedicalVisit, id=visit_id)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.visit = visit
            prescription.patient = visit.patient
            prescription.doctor = request.user
            prescription.save()
            
            # Display alerts if any
            if prescription.has_allergy_alert:
                messages.warning(request, prescription.allergy_alert_message)
            if prescription.has_conflict_alert:
                messages.warning(request, prescription.conflict_alert_message)
            
            messages.success(request, 'Prescription has been created successfully!')
            return redirect('visit_detail', visit_id=visit.id)
    else:
        form = PrescriptionForm()
    
    return render(request, 'medical/prescription_form.html', {
        'form': form,
        'visit': visit,
        'action': 'Create'
    })


@login_required
def prescription_detail(request, prescription_id):
    """
    View prescription details
    """
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    context = {
        'prescription': prescription,
    }
    return render(request, 'medical/prescription_detail.html', context)


@login_required
def prescription_deactivate(request, prescription_id):
    """
    Deactivate a prescription
    """
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    if request.method == 'POST':
        prescription.is_active = False
        prescription.save()
        messages.success(request, 'Prescription has been deactivated successfully!')
        return redirect('visit_detail', visit_id=prescription.visit.id)
    
    return render(request, 'medical/prescription_confirm_deactivate.html', {'prescription': prescription})
