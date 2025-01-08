from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
        ('registered', 'Registered User'),
        ('guest', 'Guest'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='guest')

    def __str__(self):
        return self.username
