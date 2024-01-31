from django.contrib import admin
from .models import Sponsor, StudentModel, StudentSponsor, OTM
# Register your models here.

admin.site.register(Sponsor)
admin.site.register(StudentModel)
admin.site.register(StudentSponsor)
admin.site.register(OTM)
