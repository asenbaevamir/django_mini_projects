from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=(
            "Phone number must be entered in the format: '+999999999'. "
            "Up to 15 digits allowed."
        ),
    ),
    phone_number = models.CharField(
        validators = phone_regex,
        max_length = 16,
        unique = True,
        help_text="International format, e.g. +12345678901",
    )
    def __str__(self) -> str:
        return f"{self.name, self.phone_number}"