from django.db import models


# Create your models here.
class Restaurant(models.Model):
    """Model for a restaurant."""

    name = models.CharField(max_length=50)
    website = models.CharField(max_length=100)
    TIN = models.CharField(max_length=12)
    restaurant_represenative = models.OneToOneField(
        "accounts.RestaurantRepresentative",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="restaurant",
    )


class Dish(models.Model):
    """Model for a dish."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="dishes"
    )
