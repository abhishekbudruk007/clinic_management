"""pratice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path('login', views.login, name='login'),
    path('authenticate_user', views.authenticate_user, name='authenticate_user'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('change_password', views.change_password, name='change_password'),
    path('sync_to_boto3', views.sync_to_boto3, name='sync_to_boto3'),

]
