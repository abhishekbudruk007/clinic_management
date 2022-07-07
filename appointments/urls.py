
from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "appointments"

urlpatterns = [
    path('appointment/new',views.new_appointment,name='new_appointment'),
    path('appointments/view',views.view_appointments,name='view_appointments'),
    path('appointment/<int:pk>/process',views.process_appointment,name='process_appointment'),
    path('appointment/<int:pk>/delete',views.delete_appointment,name='delete_appointment'),
    path('appointment/<int:pk>/cancel',views.cancel_appointment,name='cancel_appointment'),
    path('pending/fees',views.pending_fees,name='pending_fees'),
    path('collect/fees/<int:pk>', views.collect_fees, name="collect_fees"),
    path('payment/<int:appointment_id>/<payment_option>', views.payment, name='payment'),
    path("razorpay/callback/<int:user_id>/<int:appointment_id>", views.callback, name="callback"),
]
