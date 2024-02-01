"""Models for the wars app."""
from django.db import models
from django.utils import timezone


# Create your models here.
class War(models.Model):
    """Model for a war."""

    date = models.DateField(default=timezone.now, primary_key=True)

    @classmethod
    def get(cls) -> models.Model:
        """Return today's war."""
        return cls.objects.get(date=timezone.now().date())


class Menu(models.Model):
    """Model for a menu."""

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    wars = models.ManyToManyField(War, related_name="menus")
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", on_delete=models.CASCADE, related_name="menus"
    )
    dishes = models.ManyToManyField("restaurants.Dish", related_name="menus")


class Vote(models.Model):
    """Model for vote"""

    employee = models.ForeignKey(
        "accounts.Employee", on_delete=models.CASCADE, related_name="votes"
    )
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    war = models.ForeignKey(War, on_delete=models.CASCADE, related_name="votes")
