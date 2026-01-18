from rest_framework.routers import DefaultRouter
from .views import (
    VisitViewSet,
    DiagnosisViewSet, PrescriptionViewSet,
    LabReportViewSet
)

router = DefaultRouter()
router.register('visits', VisitViewSet)
router.register('diagnoses', DiagnosisViewSet)
router.register('prescriptions', PrescriptionViewSet)
router.register('lab-reports', LabReportViewSet)

urlpatterns = router.urls
