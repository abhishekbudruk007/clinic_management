from django.contrib import admin
from .models import NewAppointment, Payments
# Register your models here.
admin.site.register(Payments)
admin.site.register(NewAppointment)