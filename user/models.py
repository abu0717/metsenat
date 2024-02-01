from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

from .validator import validate_phone_number


# Create your models here.
class Sponsor(models.Model):
    Sponsor_Type_Choice = (
        ('Yangi', 'Yangi'),
        ('Moderatsiyada', 'Moderatsiyada'),
        ('Tasdiqlangan', 'Tasdiqlangan'),
        ('Bekor qilingan', 'Bekor qilingan')
    )
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
    support_price = models.PositiveIntegerField()
    shaxs_type = models.BooleanField(null=True, blank=True)
    orginization = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=14, choices=Sponsor_Type_Choice, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    otm_name = models.ForeignKey(OTM, on_delete=models.CASCADE, related_name='oliy')

    def __str__(self):
        return self.full_name


class StudentSponsor(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsors')
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name='students')
    summa = models.PositiveIntegerField()

    def clean(self):
        homiy_summa = StudentSponsor.objects.filter(sponsor=self.sponsor).aggregate(total_summa=Sum('summa'))[
                          'total_summa'] or 0
        std_summa = StudentSponsor.objects.filter(student=self.student).aggregate(total_summa=Sum('summa'))[
                        'total_summa'] or 0
        if (std_summa + self.summa) > self.student.contract_summa:
            raise ValidationError(
                f'The total amount is too much. You need to pay: {self.student.contract_summa - std_summa}')
        elif self.sponsor.support_price < (homiy_summa + self.summa):
            raise ValidationError(f"Sponsor doesn't have enough balance. Your balance: {self.sponsor.support_price}")

    def __str__(self):
        return self.sponsor.full_name
