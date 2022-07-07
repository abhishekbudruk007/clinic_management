from django.contrib.auth.forms import UserCreationForm
from .models import NewAppointment
from users.models import CustomUsers
from django import forms
from django.db import models


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

class My_Custom_Calender(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)


class AppointmentForm(forms.Form):
    appointment_patient = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    appointment_reason = forms.CharField(widget=forms.Textarea)
    # appointment_date = forms.DateField(widget=forms.SelectDateWidget(
    #     attrs = {'class':'form-control','placeholder':'Enter Date',"maxlength":"50",'required':'true'}))
    appointment_date = forms.DateField(widget=My_Custom_Calender(format=["%d-%m-%Y"],))
    appointment_time = forms.ChoiceField(
        widget=forms.RadioSelect, choices=TIMESLOT_LIST, required=False)

    class Meta:
        model = NewAppointment
        fields = ('appointment_patient', 'appointment_reason', 'appointment_date', 'appointment_time')


class DoctorAppointmentProcessForm(forms.ModelForm):
    appointment_patient = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}))
    appointment_reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','readonly':'readonly'}))
    appointment_time = forms.ChoiceField(
        widget=forms.RadioSelect, choices=TIMESLOT_LIST, required=False)
    appointment_remarks = forms.CharField(widget=forms.Textarea)
    appointment_medication = forms.CharField(widget=forms.Textarea)
    appointment_bill = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    appointment_followup_date = forms.DateField(widget=My_Custom_Calender(format=["%d-%m-%Y"], ))


    class Meta:
        model = NewAppointment
        fields = ('appointment_patient', 'appointment_reason', 'appointment_date', 'appointment_time',  'appointment_remarks', 'appointment_medication', 'appointment_bill', 'appointment_followup_date')


PAYMENT = (
   ('C', 'Cash'),
   ('S', 'Stripe'),
   ('R', 'Razorpay')
)


class CollectFeesForm(forms.Form):
   payment_option = forms.ChoiceField(
       widget=forms.RadioSelect, choices=PAYMENT,required=False)


PAYMENT = (
   ('C', 'Cash'),
   ('S', 'Stripe'),
   ('R', 'Razorpay')
)


class CheckoutForm(forms.Form):
   payment_option = forms.ChoiceField(
       widget=forms.RadioSelect, choices=PAYMENT,required=False)

