from django.urls import path
from rest_framework import routers

from .views import StudentViewSet, SponsorViewSet, StudentSponsorViewSet, OTMViewSet, all_sum, SponserSent

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'student_sponsor', StudentSponsorViewSet)
router.register(r'OTM', OTMViewSet)

urlpatterns = [
    path('summa/', all_sum),
    path('sponsor-create/', SponserSent.as_view(), name='')
]

urlpatterns += router.urls
