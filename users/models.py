from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
USER_TYPE = (
    ('U', 'User'),
    ('R', 'Receptionist'),
    ('D', 'Doctor'),
)

# Create your models here.
class CustomUsers(AbstractUser):
    user_type = models.CharField(choices=USER_TYPE, max_length=1, default='U')
    user_photo = models.ImageField(upload_to='users/', blank=True, null=True)