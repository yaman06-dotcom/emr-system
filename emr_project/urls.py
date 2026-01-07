"""
URL configuration for emr_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views as main_views
from accounts import views as account_views
from patients import views as patient_views
from medical import views as medical_views
from ai_prediction import views as ai_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('', account_views.login_view, name='login'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('register/', account_views.register_view, name='register'),
    path('profile/', account_views.profile_view, name='profile'),
    
    # Dashboard
    path('dashboard/', main_views.dashboard, name='dashboard'),
    
    # Patients
    path('patients/', patient_views.patient_list, name='patient_list'),
    path('patients/create/', patient_views.patient_create, name='patient_create'),
    path('patients/<int:patient_id>/', patient_views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/update/', patient_views.patient_update, name='patient_update'),
    path('patients/<int:patient_id>/delete/', patient_views.patient_delete, name='patient_delete'),
    
    # Medical Visits
    path('visits/', medical_views.visit_list, name='visit_list'),
    path('visits/create/', medical_views.visit_create, name='visit_create'),
    path('visits/create/<int:patient_id>/', medical_views.visit_create, name='visit_create_for_patient'),
    path('visits/<int:visit_id>/', medical_views.visit_detail, name='visit_detail'),
    path('visits/<int:visit_id>/update/', medical_views.visit_update, name='visit_update'),
    
    # Prescriptions
    path('prescriptions/<int:prescription_id>/', medical_views.prescription_detail, name='prescription_detail'),
    path('visits/<int:visit_id>/prescriptions/create/', medical_views.prescription_create, name='prescription_create'),
    path('prescriptions/<int:prescription_id>/deactivate/', medical_views.prescription_deactivate, name='prescription_deactivate'),
    
    # AI Predictions
    path('predictions/', ai_views.prediction_list, name='prediction_list'),
    path('patients/<int:patient_id>/predict/', ai_views.predict_risk, name='predict_risk'),
    path('predictions/<int:prediction_id>/', ai_views.prediction_detail, name='prediction_detail'),
    path('ai/train-model/', ai_views.train_model_view, name='train_model'),
]
