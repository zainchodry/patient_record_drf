from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsDoctorOrAdmin, IsPatientSelf

class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['admin', 'receptionist']:
            return Appointment.objects.all()

        if user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)

        return Appointment.objects.filter(patient__user=user)

    def perform_create(self, serializer):
        serializer.save()
