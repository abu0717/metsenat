from rest_framework import serializers
from .models import Sponsor, StudentModel, StudentSponsor, OTM


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'


class StudentSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSponsor
        fields = '__all__'

    def validate(self, data):
        instance = StudentSponsor(**data)
        instance.clean()
        return data


class OTMSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTM
        fields = '__all__'
