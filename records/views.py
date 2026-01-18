from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import (
    Visit,
    Diagnosis, Prescription, LabReport
)
from .serializers import (
    VisitSerializer,
    DiagnosisSerializer, PrescriptionSerializer,
    LabReportSerializer
)
from .permissions import IsDoctorOrAdmin


class VisitViewSet(ModelViewSet):
    queryset = Visit.objects.select_related('patient', 'doctor')
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class DiagnosisViewSet(ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]


class PrescriptionViewSet(ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]


class LabReportViewSet(ModelViewSet):
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]
