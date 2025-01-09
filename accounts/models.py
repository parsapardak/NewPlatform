from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
        ('registered', 'Registered User'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='registered')
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
