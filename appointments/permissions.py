from rest_framework.permissions import BasePermission

class IsDoctorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['doctor', 'admin']


class IsPatientSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.patient.user == request.user
