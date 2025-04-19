from django.db import models
from django.contrib.auth.models import AbstractUser

TYPES = {
    "doctor": "Doctor",
    "patient": "Patient",
}

# Create your models here.
class User(AbstractUser):

    user_type = models.CharField(
        max_length=10,
        choices=TYPES,
        default="doctor"
    )

    def __str__(self):
        return f"${self.first_name} ${self.user_type}"