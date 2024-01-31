"""Views for the restaurants app."""
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

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


class RestaurantDashboardView(DetailView, utils.RestaurantRepresetiveRequiredMixin):
    """View for showing Restaurant Details"""

    model = models.Restaurant
    template_name = "restaurants/restaurant_dashboard.html"
    context_object_name = "restaurant"

    def get_object(self, queryset: None) -> models.Restaurant:
        """Get the restaurant for the logged in user."""
        return utils.get_restaurant(self.request)
