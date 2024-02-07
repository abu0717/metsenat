from django.db.models import Sum
from rest_framework import serializers
from .models import Sponsor, StudentModel, StudentSponsor, OTM


class OTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTM
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

    def to_representation(self, instance):
        summa = StudentSponsor.objects.filter(sponsor=instance.id).aggregate(total=Sum('summa'))[
            'total'] or 0
        return {
            'id': instance.id,
            'full_name': instance.full_name,
            'phone_number': instance.phone_number,
            'organization': instance.orginization,
            'support_price': instance.support_price,
            'spent_price': summa
        }
    def validate(self, data):
        instance = Sponsor(**data)
        instance.clean()
        return data


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'

    def to_representation(self, instance):
        summa = StudentSponsor.objects.filter(student=instance.id).aggregate(total=Sum('summa'))[
            'total'] or 0
        return {
            'id': instance.id,
            'full_name': instance.full_name,
            'otm': instance.otm_name.otm_name,
            'phone_number': instance.phone_number,
            'contract_sum': instance.contract_summa,
            'payed_price': summa,
        }


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'

    def to_representation(self, instance):
        summa = StudentSponsor.objects.filter(student=instance.id).aggregate(total_summa=Sum('summa'))[
                    'total_summa'] or 0
        student_homiylari = StudentSponsor.objects.filter(student=instance.id).values_list('sponsor', flat=True)
        student_homiylari = Sponsor.objects.filter(id__in=student_homiylari).values()
        return {
            'id': instance.id,
            'full_name': instance.full_name,
            'otm': instance.otm_name.otm_name,
            'phone_number': instance.phone_number,
            'contract_sum': instance.contract_summa,
            'payed_price': summa,
            'student_homiylari': student_homiylari
        }

    def validate(self, data):
        instance = StudentModel(**data)
        instance.clean()
        return data


class StudentSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSponsor
        fields = '__all__'

    def validate(self, data):
        instance = StudentSponsor(**data)
        instance.clean()
        return data
