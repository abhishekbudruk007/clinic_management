from django.db import models
# Create your models here.
from django.conf import settings
PAYMENT = (
  ('C', 'Cash'),
  ('S', 'Stripe'),
  ('R', 'Razorpay')
)

TIMESLOT_LIST = (
        (0, '09:00 – 09:30'),
        (1, '10:00 – 10:30'),
        (2, '11:00 – 11:30'),
        (3, '12:00 – 12:30'),
        (4, '13:00 – 13:30'),
        (5, '14:00 – 14:30'),
        (6, '15:00 – 15:30'),
        (7, '16:00 – 16:30'),
        (8, '17:00 – 17:30'),
    )

class Payments(models.Model):
    provider_order_id = models.CharField(max_length=40, null=True, blank=True, default="")
    payment_id = models.CharField(max_length=36, null=True, blank=True, default="")
    signature_id = models.CharField(max_length=128, null=True, blank=True, default="")
    payment_type = models.CharField(choices=PAYMENT, default="", null=True, blank=True, max_length=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.user.username

class NewAppointment(models.Model):
    appointment_patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment_reason = models.TextField(max_length=500, null=False, blank=False)
    appointment_created_date = models.DateTimeField(auto_now_add=True)
    appointment_updated_date = models.DateTimeField(auto_now=True)
    appointment_date = models.DateField(blank=False, null=False)
    appointment_time = models.IntegerField(choices=TIMESLOT_LIST)
    appointment_completed = models.BooleanField(default=False)
    appointment_iscancelled = models.BooleanField(default=False)
    appointment_remarks = models.TextField(max_length=500, null=True, blank=True)
    appointment_medication = models.TextField(max_length=500, null=True, blank=True)
    appointment_bill = models.FloatField(default=0.0, null=True, blank=True)
    appointment_followup_date = models.DateField(null=True, blank=True)
    paid= models.BooleanField(default=False)
    payment = models.ForeignKey(
        'Payments', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{} {} . Patient: {}'.format(self.appointment_date, self.appointment_time, self.appointment_patient.username)


    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


