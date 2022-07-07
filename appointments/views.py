from .models import NewAppointment, TIMESLOT_LIST
from .forms import AppointmentForm, DoctorAppointmentProcessForm, CollectFeesForm, CheckoutForm
from users.models import CustomUsers
from django.shortcuts import redirect, render
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Payments
import razorpay
from clinic.utils import send_an_email

TIMESLOT_DICT = {
        0 : '09:00 – 09:30',
        1 : '10:00 – 10:30',
        2 : '11:00 – 11:30',
        3 : '12:00 – 12:30',
        4 : '13:00 – 13:30',
        5 : '14:00 – 14:30',
        6 : '15:00 – 15:30',
        7 : '16:00 – 16:30',
        8 : '17:00 – 17:30',
    }


@login_required
def new_appointment(request):
    if request.method == 'POST':
        appointment_patient = request.POST.get('appointment_patient', '')
        appointment_reason = request.POST.get('appointment_reason','')
        appointment_date = request.POST.get('appointment_date','')
        appointment_date = datetime.datetime.strptime(appointment_date, "%Y-%m-%d")
        if appointment_date.date() < datetime.datetime.now().date():
            messages.error(request, "Select date in future")
            return redirect('appointments:new_appointment')
        appointment_time = request.POST.get('appointment_time')
        appointment_object = NewAppointment.objects.filter(appointment_date=appointment_date, appointment_time=appointment_time, appointment_completed=False)
        if appointment_object:
            messages.error(request, "Appointment cannot be booked for this Slot , as its already full")
            return redirect('appointments:new_appointment')
        else:
            appointment_object = NewAppointment()
            if request.user.user_type == "U":
                # This is when user is logged in and booking appointment for himself
                appointment_object.appointment_patient = request.user
            else:
                # This is when receptionist is logged in and booking appointment for patients/users
                if appointment_patient:
                    appointment_patient = CustomUsers.objects.filter(username=appointment_patient)[0]
                appointment_object.appointment_patient = appointment_patient
            appointment_object.appointment_reason = appointment_reason
            appointment_object.appointment_date = appointment_date.date()
            appointment_object.appointment_time = appointment_time
            appointment_object.save()
            messages.error(request, "Appointment Booked Successfully")
            return redirect('appointments:new_appointment')
    else:
        form = AppointmentForm()
        user_objects = CustomUsers.objects.filter(user_type='U', is_staff=False)
        print("user_objects",user_objects)
        todays_date = datetime.datetime.now()
        todays_date = todays_date.strftime("%Y-%m-%d")
        if request.user.user_type == "U":
            appointments_objects = NewAppointment.objects.filter(appointment_patient = request.user, appointment_date=todays_date, appointment_completed=False)
        else:
            appointments_objects = NewAppointment.objects.filter(appointment_date=todays_date,
                                                                 appointment_completed=False)
        return render(request, 'appointments/new_appointment.html', {'form': form, 'appointments': appointments_objects, 'users':user_objects, 'timeslot': TIMESLOT_DICT})

@login_required
def view_appointments(request):

    todays_date = datetime.datetime.now()
    todays_date =todays_date.strftime("%Y-%m-%d")
    if request.user.user_type == "U":
        completed_appointments_objects = NewAppointment.objects.filter(appointment_patient = request.user, appointment_completed=True, appointment_iscancelled=False).order_by('-appointment_updated_date')
        future_appointments_objects = NewAppointment.objects.filter(appointment_patient = request.user, appointment_date__gte=todays_date,appointment_completed=False, appointment_iscancelled=False).order_by('appointment_date','appointment_time')
    else:
        completed_appointments_objects = NewAppointment.objects.filter(appointment_completed=True, appointment_iscancelled=False).order_by('-appointment_updated_date')
        future_appointments_objects = NewAppointment.objects.filter(appointment_date__gte=todays_date,appointment_completed=False, appointment_iscancelled=False).order_by('appointment_date','appointment_time')
    return render(request, "appointments/view_appointments.html", {'completed_appointments': completed_appointments_objects, "future_appointments":future_appointments_objects, 'timeslot': TIMESLOT_DICT})



@login_required
def process_appointment(request, pk):  # id
    submitted_appointment = get_object_or_404(NewAppointment, id=pk)
    # import pdb;pdb.set_trace()
    form = DoctorAppointmentProcessForm(instance=submitted_appointment)
    if request.method == "POST":
        # import pdb;pdb.set_trace()
        # form = DoctorAppointmentProcessForm(request.POST, instance=submitted_appointment)
        appointment_patient = request.POST.get('appointment_patient', '')
        patient_object = CustomUsers.objects.filter(id=appointment_patient)[0]
        appointment_reason = request.POST.get('appointment_reason', '')
        appointment_date = request.POST.get('appointment_date', '')
        appointment_date = datetime.datetime.strptime(appointment_date, "%Y-%m-%d")
        appointment_time = request.POST.get('appointment_time')
        appointment_remarks = request.POST.get('appointment_remarks', '')
        appointment_medication = request.POST.get('appointment_medication', '')
        appointment_bill = request.POST.get('appointment_bill', '')
        appointment_followup_date = request.POST.get('appointment_followup_date', '')
        appointment_followup_date = datetime.datetime.strptime(appointment_followup_date, "%Y-%m-%d")
        # if form.is_valid():
        # form.save(commit=True)
        # processed_appoinment = form.save(commit=False)
        processed_appoinment = NewAppointment.objects.filter(appointment_patient = appointment_patient, appointment_date=appointment_date, appointment_time=appointment_time)[0]
        processed_appoinment.appointment_patient = patient_object
        processed_appoinment.appointment_remarks = appointment_remarks
        processed_appoinment.appointment_medication = appointment_medication
        processed_appoinment.appointment_bill = appointment_bill
        processed_appoinment.appointment_followup_date = appointment_followup_date
        processed_appoinment.appointment_completed = True
        processed_appoinment.save()
        messages.success(request,"Appointment Completed")
        return redirect('appointments:view_appointments')
    else:
        return render(request, 'appointments/process_appointment.html', {'form': form})



def delete_appointment(request, pk):
    try:
        appointment_object = get_object_or_404(NewAppointment, id=pk)
        appointment_object.delete()
        messages.error(request, "Appointment Deleted Successfully")
    except Exception as e:
        print(e)
        messages.error(request, "Error Occurred while deleting Appointment")
    return redirect('appointments:view_appointments')


@login_required
def cancel_appointment(request, pk):  # id
    # import pdb;pdb.set_trace()
    active_appointments = NewAppointment.objects.filter(id=pk, appointment_iscancelled=False)
    try:
        if active_appointments:
            submitted_appointment = active_appointments[0]
            submitted_appointment.appointment_iscancelled = True
            submitted_appointment.save()
            messages.error(request, "Appointment has been cancelled")
    except Exception as e:
        print(e)
        messages.error(request, "Error Occurred While Cancelling Appointment")
    return redirect('appointments:view_appointments')

@login_required
def pending_fees(request):
    context = {}
    if request.user.user_type == "U":
        completed_appointments_objects = NewAppointment.objects.filter(appointment_patient=request.user,
                                                                       appointment_completed=True,
                                                                       appointment_iscancelled=False, paid=False).order_by(
            '-appointment_updated_date')

    else:
        completed_appointments_objects = NewAppointment.objects.filter(appointment_completed=True,
                                                                       appointment_iscancelled=False, paid=False).order_by(
            '-appointment_updated_date')


    return render(request, 'appointments/pending_fees.html', {'completed_appointments': completed_appointments_objects, 'timeslot': TIMESLOT_DICT})


@login_required
def collect_fees(request, pk):
   # import pdb;pdb.set_trace()
   if request.method == "POST":
       form = CheckoutForm(request.POST or None)
       try:
           if form.is_valid():
               payment_option = form.cleaned_data.get('payment_option')
               if payment_option == 'C':
                   return redirect('appointments:payment', appointment_id=pk , payment_option='C')
               elif payment_option == 'S':
                   return redirect('appointments:payment', appointment_id=pk, payment_option='S')
               elif payment_option == 'R':
                   return redirect('appointments:payment', appointment_id=pk ,payment_option='R')
               else:
                   messages.warning(request, "Invalid Payment option")
                   return redirect('appointments:collect_fees', pk = pk)

       except Exception as e:
           messages.error(request, "You do not have an order")
       return redirect("appointments:pending_fees")
   else:
       form = CheckoutForm()
       # order = Order.objects.get(user=request.user, ordered=False)
       context = {
           'form': form,
           # 'order': order
       }
       return render(request, 'appointments/collect_fees.html', context)




from clinic.utils import send_an_email_with_html
@login_required
def payment(request, appointment_id, payment_option):
    # import pdb;pdb.set_trace()
    appointment = NewAppointment.objects.filter(id=appointment_id, appointment_completed=True)[0]
    if payment_option == "C":
        payment_object = Payments()
        payment_object.user = appointment.appointment_patient
        payment_object.payment_type = payment_option
        payment_object.amount = appointment.appointment_bill
        payment_object.save()
        appointment.payment = payment_object
        appointment.paid = True
        appointment.save()
        messages.success(request, "Fees Paid Successfully")
        send_an_email_with_html(request, 'abhishek.budruk@gmail.com', appointment )
        return redirect('appointments:pending_fees')
    if payment_option == "R":
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(appointment.appointment_bill) * 100, "currency": "INR", "payment_capture": "1"}
        )
        payment_object = Payments()
        payment_object.provider_order_id = razorpay_order['id']
        payment_object.user = appointment.appointment_patient
        payment_object.payment_type = payment_option
        payment_object.amount = appointment.appointment_bill
        payment_object.save()
        appointment.payment = payment_object
        appointment.save()
        return render(
            request,
            "appointments/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "appointment": appointment,
                "user": appointment.appointment_patient
            },
        )


from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def callback(request, user_id, appointment_id):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)
    # import pdb;pdb.set_trace()
    user = CustomUsers.objects.filter(id=user_id)
    if user:
        user = user[0]
        appointment = NewAppointment.objects.filter(appointment_patient=user, id = appointment_id,  paid=False)[0]
        if "razorpay_signature" in request.POST:
            payment_id = request.POST.get("razorpay_payment_id", "")
            provider_order_id = request.POST.get("razorpay_order_id", "")
            signature_id = request.POST.get("razorpay_signature", "")

            payment_object = Payments.objects.get(provider_order_id=provider_order_id)
            payment_object.payment_id = payment_id
            payment_object.signature_id = signature_id
            payment_object.save()

            if verify_signature(request.POST):
                appointment.paid = True
                appointment.save()
                return render(request, "appointments/callback.html", context={"status": appointment.paid, "user":user})
            else:
                appointment.paid = False
                appointment.save()
                return render(request, "appointments/callback.html", context={"status": appointment.paid, "user":user})
        else:
            payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
            provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
                "order_id"
            )
            payment_object = Payments.objects.get(provider_order_id=provider_order_id)
            payment_object.payment_id = payment_id
            payment_object.save()
            return render(request, "appointments/callback.html", context={"status": appointment.paid, "user":user})



