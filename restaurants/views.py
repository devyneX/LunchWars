"""Views for the restaurants app."""
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpRequest
from django.views import View
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from . import utils
from . import models


# Create your views here.
class RestaurantCreateView(CreateView, utils.RestaurantRepresetiveRequiredMixin):
    """View for creating a restaurant."""

    model = models.Restaurant
    fields = ["name", "website", "TIN"]
    success_url = reverse_lazy("restaurants:dashboard")
    template_name = "restaurants/create.html"

    def invalid_tin(self, form: BaseModelForm, error: str) -> HttpResponse:
        """Return an error message."""
        form.add_error("TIN", error)
        return super().form_invalid(form)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Save the restaurant representative."""
        # validate TIN number
        is_tin_valid = utils.validate_tin(form.instance.TIN)
        if is_tin_valid:
            form.instance.restaurant_represenative = (
                self.request.user.restaurant_representative
            )
            return super().form_valid(form)

        return self.invalid_tin(form, "TIN number is not valid.")


class RestaurantDashboardView(View, utils.RestaurantRepresetiveRequiredMixin):
    """View for showing Restaurant Details"""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Return the restaurant details."""
        restaurant = utils.get_restaurant(request)
        if not restaurant:
            return redirect("restaurants:create")
        return render(
            request,
            "restaurants/dashboard.html",
            {"restaurant": restaurant},
        )


class AddDishView(CreateView, utils.RestaurantRepresetiveRequiredMixin):
    """View for adding a dish."""

    model = models.Dish
    fields = ["name", "description"]
    success_url = reverse_lazy("restaurants:dashboard")
    template_name = "restaurants/add_dish.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Save the dish."""
        restaurant = utils.get_restaurant(self.request)
        form.instance.restaurant = restaurant
        return super().form_valid(form)


# class EditDishView(UpdateView, utils.RestaurantRepresetiveRequiredMixin):
#     """View for editing a dish."""

#     model = models.Dish
#     fields = ["name", "description"]
#     success_url = reverse_lazy("restaurants:dashboard")
#     template_name = "restaurants/edit_dish.html"

#     def get_queryset(self):
#         """Get the dishes for the restaurant."""
#         restaurant = utils.get_restaurant(self.request)
#         return models.Dish.objects.filter(restaurant=restaurant)


class DishListView(ListView, utils.RestaurantRepresetiveRequiredMixin):
    """View for listing dishes."""

    model = models.Dish
    template_name = "restaurants/dishes.html"
    context_object_name = "dishes"
    success_url = reverse_lazy("restaurants:dishes")

    def get_queryset(self):
        """Get the dishes for the restaurant."""
        restaurant = utils.get_restaurant(self.request)
        return models.Dish.objects.filter(restaurant=restaurant)
