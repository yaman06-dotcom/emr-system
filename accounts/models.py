from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based access control
    Roles: Doctor, Admin
    """
    ROLE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='DOCTOR')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_doctor(self):
        return self.role == 'DOCTOR'
    
    def is_admin(self):
        return self.role == 'ADMIN'
