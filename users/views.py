from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import RegistrationForm
from.models import CustomUsers
from django.contrib.auth.hashers import make_password,check_password
import os
from django.conf import settings
from clinic.utils import send_an_email
# Create your views here.
def login(request):
    # return HttpResponse("this is Login page"),
    return render(request, 'users/login.html')



def authenticate_user(request):
    username_str = request.POST.get('username')
    password_str = request.POST.get('password')
    if username_str and password_str:
        try:
            user = authenticate(username=username_str, password=password_str)
        except:
            messages.error(request, "username/password is Incorrect")
            return HttpResponseRedirect('login')
        if user is not None:
            auth_login(request, user)
            request.session['username'] = username_str
            if request.user.user_type == "D":
                messages.success(request, f"Doctor {request.user.username} has Logged In")
                return redirect("appointments:view_appointments")
            elif request.user.user_type == "R":
                messages.success(request, f"Receptionist {request.user.username} has Logged In")
                return redirect("appointments:view_appointments")
            else:
                return redirect("appointments:new_appointment")
        else:
            messages.error(request, "username/password is incorrect")
            return redirect('users:login')
    else:
        messages.error(request, "enter username or password")
        return redirect('users:login')

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return HttpResponseRedirect('login')
    return redirect('users:login')


def register(request):
    registration_form = RegistrationForm()
    # return HttpResponse('register page')
    if request.method == "POST":
        registration_form = RegistrationForm(request.POST, request.FILES)
        if registration_form.is_valid():
            registration_form.save()
            messages.success(request,"Registration is Successfull")
            return HttpResponseRedirect("login")
        else:
            # messages.error(request,'Registration unsucessfull')
            return HttpResponseRedirect("register")
    else:
        return render(request, 'users/register.html', context={"form":registration_form})


def change_password(request):
    if request.method == "POST":
        # import pdb:
        # pdb.set_trace()
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        users_object = CustomUsers.objects.filter(username=request.user.username)[0]
        if check_password(old_password, users_object.password):
            users_object.password = make_password(new_password)
            users_object.save()
        return HttpResponseRedirect('login')

    else:
        return render(request,'users/change_password.html')



import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIA5R5UV6XBCFXPRLXT'
SECRET_KEY = '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'


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def sync_to_boto3(request):
    # import pdb;pdb.set_trace()
    local_file_name =  os.path.join(settings.BASE_DIR, 'db.sqlite3')
    uploaded = upload_to_aws(local_file_name, 'clinicbucket2022', 'db.sqlite3')
    if uploaded:
        messages.success(request, "You data is Syncd Successfully")
        return redirect('dashboard:home')
    else:
        messages.error(request, "Your Data Cannot be Syncd ")
        return redirect('dashboard:home')