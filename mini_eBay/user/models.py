from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        BUYER = 'buyer', 'Покупатель'
        SELLER = 'seller', 'Продавец'

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=(
            "Phone number must be entered in the format: '+999999999'. "
            "Up to 15 digits allowed."
        ),
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=16,
        blank=True,
        null=True,
        help_text="International format, e.g. +12345678901",
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.BUYER,
    )

    def is_seller(self):
        return self.role == self.Role.SELLER

    def is_buyer(self):
        return self.role == self.Role.BUYER

    def __str__(self) -> str:
        return self.username