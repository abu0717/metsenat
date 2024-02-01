from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import filters, pagination, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from .serializers import StudentSerializer, StudentSponsorSerializer, SponsorSerializer, OTMSerializer
from .models import StudentModel, StudentSponsor, Sponsor, OTM
from rest_framework.permissions import IsAdminUser, BasePermission


# Create your views here.
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 10
    max_page_size = 10


class StudentViewSet(ModelViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['education_type', 'otm_name__otm_name']


class StudentSponsorViewSet(ModelViewSet):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer
    permission_classes = [IsAdminUser]


class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination
    search_fields = ['support_price', 'status', 'created_at']


class OTMViewSet(ModelViewSet):
    queryset = OTM.objects.all()
    serializer_class = OTMSerializer
    permission_classes = [IsAdminUser]


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'


@api_view(['GET'])
@permission_classes([CustomPermission])
def all_sum(request):
    homiy_tolagan = StudentSponsor.objects.all().values_list('summa', flat=True)
    student_soragan = StudentModel.objects.all().values_list('contract_summa', flat=True)
    homiy_tolagan = sum(homiy_tolagan)
    student_soragan = sum(student_soragan)
    qolgan = student_soragan - homiy_tolagan
    return Response({
        'status_code': 200,
        'info': {
            'homiy_tolagan': homiy_tolagan,
            'student_soragan': student_soragan,
            'qolgan': qolgan
        }
    })
