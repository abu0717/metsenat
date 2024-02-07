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
            'support_price': instance.support_price,
            'spent_price': summa,
            'date': instance.created_at,
            'status': instance.status
        }

    def validate(self, data):
        instance = Sponsor(**data)
        instance.clean()
        return data


class SponsorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

    def to_representation(self, instance):
        if instance.orginization == '':
            return {
                'id': instance.id,
                'full_name': instance.full_name,
                'phone_number': instance.phone_number,
                'support_price': instance.support_price,
                'status': instance.status
            }
        else:
            return {
                'id': instance.id,
                'full_name': instance.full_name,
                'phone_number': instance.phone_number,
                'support_price': instance.support_price,
                'organization': instance.orginization,
                'status': instance.status
            }


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
            'study_type': instance.education_type,
            'otm': instance.otm_name.otm_name,
            'payed_price': summa,
            'contract_sum': instance.contract_summa
        }


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'

    def to_representation(self, instance):
        student_sponsors = StudentSponsor.objects.filter(student=instance.id)
        summa = student_sponsors.aggregate(total_summa=Sum('summa'))['total_summa'] or 0
        student_homiylari = []
        for sponsor in student_sponsors:
            sponsor_info = {
                'id': sponsor.sponsor.id,
                'full_name': sponsor.sponsor.full_name,
                'spent_price': sponsor.summa
            }
            student_homiylari.append(sponsor_info)
        return {
            'id': instance.id,
            'full_name': instance.full_name,
            'phone_number': instance.phone_number,
            'otm': instance.otm_name.otm_name,
            'study_type': instance.education_type,
            'payed_price': summa,
            'contract_sum': instance.contract_summa,
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
