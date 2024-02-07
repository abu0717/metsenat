from django.db.models import Sum
from rest_framework import filters, pagination, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from .serializers import StudentSerializer, StudentDetailSerializer, StudentSponsorSerializer, SponsorSerializer, \
    OTMSerializer, SponsorDetailSerializer
from .models import StudentModel, StudentSponsor, Sponsor, OTM
from rest_framework.permissions import IsAdminUser, BasePermission


# Create your views here.
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 10
    max_page_size = 10


# class StudentViewSet(ModelViewSet):
#     queryset = StudentModel.objects.all()
#     serializer_class = StudentSerializer
#     permission_classes = [IsAdminUser]
#     pagination_class = CustomPagination
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['education_type', 'otm_name__otm_name']
#     http_method_names = ['get', 'patch', 'post', 'delete']

class StudentView(generics.ListCreateAPIView):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['education_type', 'otm_name__otm_name']


class Student(generics.RetrieveUpdateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = StudentModel.objects.all()
    serializer_class = StudentDetailSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'patch', 'head', 'delete']


class StudentSponsorViewSet(ModelViewSet):
    queryset = StudentSponsor.objects.all()
    serializer_class = StudentSponsorSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'patch', 'post', 'delete']


class SponsorViewSet(ModelViewSet, generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    search_fields = ['support_price', 'status', 'created_at']
    http_method_names = ['get', 'patch', 'delete']


class SponsorDetail(generics.RetrieveUpdateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorDetailSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'patch', 'delete']


class OTMViewSet(ModelViewSet):
    queryset = OTM.objects.all()
    serializer_class = OTMSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'patch', 'delete', 'post']


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'


@api_view(['GET'])
@permission_classes([CustomPermission])
def all_sum(request):
    homiy_summa = StudentSponsor.objects.all().aggregate(total_summa=Sum('summa'))[
                      'total_summa'] or 0
    std_summa = StudentSponsor.objects.filter().aggregate(total_summa=Sum('summa'))[
                    'total_summa'] or 0
    qolgan = std_summa - homiy_summa
    return Response({
        'status_code': 200,
        'info': {
            'homiy_tolagan': homiy_summa,
            'student_soragan': std_summa,
            'qolgan': qolgan
        }
    })


class SponserSent(generics.GenericAPIView, mixins.CreateModelMixin):
    queryset = StudentSponsor.objects.all()
    serializer_class = SponsorSerializer

    def post(self, request):
        return self.create(request)
