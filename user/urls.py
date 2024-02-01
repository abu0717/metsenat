from django.urls import path
from rest_framework import routers

from .views import StudentViewSet, SponsorViewSet, StudentSponsorViewSet, OTMViewSet, all_sum

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'student_sponsor', StudentSponsorViewSet)
router.register(r'OTM', OTMViewSet)

urlpatterns = [
    path('summa/', all_sum)
]

urlpatterns += router.urls
