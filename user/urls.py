from django.urls import path
from rest_framework import routers

from .views import StudentViewSet, SponsorViewSet, StudentSponsorViewSet, OTMViewSet

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'student_sponsor', StudentSponsorViewSet)
router.register(r'OTM', OTMViewSet)

urlpatterns = router.urls
