from django.db import models

# Create your models here.
import uuid
from django.db import models 
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Uses UUID as primary key and adds additional fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('amin', "Admin"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    REQUIRED_FIELDS = ['email'] # email required on creates

    def __str__(self):
        return f"{self.username} ({self.email})"
    

