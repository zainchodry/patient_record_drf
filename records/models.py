from django.db import models
from accounts.models import User, PatientProfile

class Visit(models.Model):
    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="visits"
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="doctor_visits"
    )

    visit_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Visit - {self.patient.user.email}"


class Diagnosis(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name="diagnoses"
    )

    diagnosis = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.diagnosis[:30]


class Prescription(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )

    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return self.medicine_name

class LabReport(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name="lab_reports"
    )

    test_name = models.CharField(max_length=100)
    report_file = models.FileField(upload_to="lab_reports/")
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name
