from django.urls import path
from rest_framework import routers

from .views import Student, SponsorViewSet, StudentSponsorViewSet, OTMViewSet, all_sum, SponserSent, StudentView, \
    SponsorDetail

router = routers.DefaultRouter()
# router.register(r'students', StudentViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'student_sponsor', StudentSponsorViewSet)
router.register(r'OTM', OTMViewSet)

urlpatterns = [
    path('summa/', all_sum),
    path('sponsor-create/', SponserSent.as_view(), name=''),
    path('students/', StudentView.as_view(), name=''),
    path('students/<int:pk>/', Student.as_view(), name=''),
    path('sponsors/<int:pk>/', SponsorDetail.as_view())

]

urlpatterns += router.urls
