from rest_framework import serializers
from .models import (
    Visit, Diagnosis,
    Prescription, LabReport
)

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"


class LabReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabReport
        fields = "__all__"


class VisitSerializer(serializers.ModelSerializer):
    diagnoses = DiagnosisSerializer(many=True, read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    lab_reports = LabReportSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = "__all__"
        read_only_fields = ['doctor']
