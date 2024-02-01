from django.shortcuts import render
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from .serializers import StudentSerializer, StudentSponsorSerializer, SponsorSerializer, OTMSerializer
from .models import StudentModel, StudentSponsor, Sponsor, OTM
from rest_framework.permissions import IsAdminUser


# Create your views here.

class StudentViewSet(ModelViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['education_type']


class StudentSponsorViewSet(ModelViewSet):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer
    permission_classes = [IsAdminUser]


class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['support_price']


class OTMViewSet(ModelViewSet):
    queryset = OTM.objects.all()
    serializer_class = OTMSerializer
    permission_classes = [IsAdminUser]
