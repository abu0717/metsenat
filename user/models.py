from django.db import models
from django.core.exceptions import ValidationError
from .validator import validate_phone_number


# Create your models here.
class Sponsor(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
    support_price = models.PositiveIntegerField()
    shaxs_type = models.BooleanField()
    orginization = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class OTM(models.Model):
    otm_name = models.CharField(max_length=100)

    def __str__(self):
        return self.otm_name


class StudentModel(models.Model):
    STUDENT_CHOICES = (
        ('B', 'Bakalavir'),
        ('M', 'Magistratura')
    )
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
    education_type = models.CharField(max_length=1, choices=STUDENT_CHOICES)
    contract_summa = models.PositiveIntegerField(default=0)
    otm_name = models.ForeignKey(OTM, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class StudentSponsor(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsors')
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name='students')
    summa = models.PositiveIntegerField()

    def clean(self):
        homiy = StudentSponsor.objects.filter(sponsor=self.sponsor).values_list('summa', flat=True)
        std = StudentSponsor.objects.filter(student=self.student).values_list('summa', flat=True)
        homiy_summa = sum(homiy)
        std_summa = sum(std)
        print('holla')
        if (self.summa + std_summa) > self.sponsor.support_price:
            raise ValidationError(f'It too much. \n need to pay:{self.sponsor.support_price - std_summa}')
        elif self.sponsor.support_price < homiy_summa:
            raise ValidationError(f"Sponsor doesn't have enough.\n Balance:{self.sponsor.support_price - homiy_summa}")

    def __str__(self):
        return self.sponsor.full_name
