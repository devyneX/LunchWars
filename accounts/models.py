"""Models for accounts app."""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model."""

    is_employee = models.BooleanField(default=False)
    is_restaurant_representative = models.BooleanField(default=False)


class Employee(models.Model):
    """Model for employee."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee", primary_key=True
    )


class RestaurantRepresentative(models.Model):
    """Model for restaurant representative."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="restaurant_representative",
        primary_key=True,
    )
