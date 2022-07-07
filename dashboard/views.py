from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clinic.utils import send_an_email
@login_required
def home(request):
    # print('this is home page')
    return render(request, 'home/index.html')
def about(request):
    # print('this is about page')
    return render(request, 'home/about.html')

