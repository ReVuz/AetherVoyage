from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_staff_member(self):
        return self.role in ['staff', 'admin'] or self.is_staff

    @property
    def is_customer(self):
        return self.role == 'customer'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
