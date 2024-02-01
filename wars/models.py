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

    @classmethod
    def eligible(cls, restaurant: "restaurants.Restaurant") -> bool:
        """Check if a restaurant is eligible for the war."""
        yesteday = timezone.now().date() - timezone.timedelta(days=1)
        the_day_before = timezone.now().date() - timezone.timedelta(days=2)

        winner_yesterday = cls.objects.filter(date=yesteday).first()
        if winner_yesterday is None:
            return True
        winner_yesterday = (
            winner_yesterday.menus.all()
            .annotate(votes_count=models.Count("votes"))
            .order_by("-votes_count")
            .first()
        )
        winner_the_day_before = cls.objects.filter(date=the_day_before).first()
        if winner_the_day_before is None:
            return True
        winner_the_day_before = (
            winner_the_day_before.menus.all()
            .annotate(votes_count=models.Count("votes"))
            .order_by("-votes_count")
            .first()
        )

        if (
            restaurant.id
            == winner_yesterday.restaurant.id
            == winner_the_day_before.restaurant.id
        ):
            return False


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
