from django.contrib import admin
from .models import CustomUsers
from .forms import CustomUserForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUsers
    add_form = CustomUserForm
    list_display = ['username','user_type','first_name','last_name','is_staff']
    list_filter = ['user_type']
    fieldsets = (*UserAdmin.fieldsets,
                 (
                     'upload user photo',
                     {
                         'fields':('user_photo','user_type')
                     }
                 )
                 )
admin.site.register(CustomUsers,CustomUserAdmin)