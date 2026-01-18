from rest_framework.routers import DefaultRouter
from . views import *

router = DefaultRouter()

router.register('notifications', NotificationViewSet, basename='notifications')

urlpatterns = router.urls

