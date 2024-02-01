"""Utility functions for the restaurants app."""
# import requests
# from django.conf import settings
from django.http import HttpRequest
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from . import models


class RestaurantRepresentiveRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for views that require a restaurant representative."""

    def test_func(self) -> bool:
        """Test if the user is a restaurant representative."""
        return self.request.user.is_restaurant_representative


def validate_tin(tin: str) -> bool:
    """Validate TIN number.

    Args:
        tin (str): The TIN number to be validated.

    Returns:
        bool: True if the TIN number is valid, False otherwise.
    """
    # this needs more testing
    # url = settings.TIN_VALIDATOR_URL
    # params = {"tk": settings.TIN_VALIDATOR_TOKEN, "op": "tc", "ca": "bd", "tn": tin}

    # response = requests.get(url, params=params)

    # if response.status_code != 200:
    #     return False

    # return response.json()["result"] == "valid"
    return True


def get_restaurant(request: HttpRequest) -> models.Restaurant:
    """Get the restaurant for the logged in user."""
    return request.user.restaurant_representative.restaurant
