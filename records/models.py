from django.db import models
from accounts.models import User
from accounts.models import Profile

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='records')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    