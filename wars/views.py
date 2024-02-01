"""Views for the wars app."""
from typing import Any
from django.db.models.query import QuerySet
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.forms.models import BaseModelForm
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from restaurants import utils as restaurant_utils
from restaurants import models as restaurant_models
from employees import utils as employee_utils
from . import models
from . import forms


# Create your views here.
class Participate(View, restaurant_utils.RestaurantRepresentiveRequiredMixin):
    """View for participating in a war."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Return the participate page."""
        menu = (
            models.War.get()
            .menus.filter(restaurant=restaurant_utils.get_restaurant(request))
            .first()
        )

        if not menu:
            return redirect("wars:create-menu")

        if menu.dishes.count() == 0:
            return redirect("wars:add-to-menu")

        return redirect("wars:menu-detail", menu.pk)


class MenuCreateView(CreateView, restaurant_utils.RestaurantRepresentiveRequiredMixin):
    """View for creating a menu."""

    model = models.Menu
    fields = ["title", "description"]
    success_url = reverse_lazy("wars:add-to-menu")
    template_name = "wars/create_menu.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Return the create menu page."""
        menu = (
            models.War.get()
            .menus.filter(restaurant=restaurant_utils.get_restaurant(self.request))
            .first()
        )
        if menu:
            if menu.dishes.count() == 0:
                return redirect("wars:add-to-menu")
            else:
                return redirect("wars:menu-detail", menu.pk)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Save the menu."""
        menu = form.save(commit=False)
        menu.restaurant = restaurant_utils.get_restaurant(self.request)
        menu.save()
        menu.wars.add(models.War.get())
        return redirect("wars:add-to-menu")


class AddToMenuView(ListView, restaurant_utils.RestaurantRepresentiveRequiredMixin):
    """View for adding dishes to a menu."""

    model = restaurant_models.Dish
    template_name = "wars/add_to_menu.html"
    context_object_name = "dishes"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Return the dishes for the current restaurant."""
        menu = (
            models.War.get()
            .menus.filter(restaurant=restaurant_utils.get_restaurant(self.request))
            .first()
        )
        if not menu:
            return redirect("wars:create-menu")

        if menu.dishes.count() > 0:
            return redirect("wars:menu-detail", menu.pk)

        self.menu = menu
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        """Return the dishes for the current restaurant."""
        queryset = super().get_queryset()
        return queryset.filter(restaurant=restaurant_utils.get_restaurant(self.request))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Return the context data."""
        DishSelectionFormSet = modelformset_factory(
            restaurant_models.Dish, form=forms.AddToMenuForm, extra=0
        )
        formset = DishSelectionFormSet(queryset=self.get_queryset())
        dishes_and_forms = zip(self.get_queryset(), formset)
        context = super().get_context_data(**kwargs)
        context["menu"] = self.menu
        context["formset"] = formset
        context["dishes_and_forms"] = dishes_and_forms
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Save the menu."""
        menu = (
            models.War.get()
            .menus.filter(restaurant=restaurant_utils.get_restaurant(self.request))
            .first()
        )
        if not menu:
            return redirect("wars:create-menu")

        DishSelectionFormSet = modelformset_factory(
            restaurant_models.Dish, form=forms.AddToMenuForm, extra=0
        )
        formset = DishSelectionFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data["selected"]:
                    menu.dishes.add(form.instance)

        if menu.dishes.count() == 0:
            messages.error(request, "You must select at least one dish.")
            return redirect("wars:add-to-menu")

        return redirect("wars:leaderboard")


class MenuDetailView(DetailView, LoginRequiredMixin):
    """View for showing the menu."""

    model = models.Menu
    template_name = "wars/menu_detail.html"
    context_object_name = "menu"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Return the context data."""
        context = super().get_context_data(**kwargs)
        context["dishes"] = self.object.dishes.all()
        if self.request.user.is_employee:
            context["voted"] = self.object.votes.filter(
                employee=self.request.user.employee
            ).exists()
        return context


class ParticipantView(ListView, employee_utils.EmployeeRequiredMixin):
    """View for showing the participant."""

    model = models.Menu
    template_name = "wars/participants.html"
    context_object_name = "menus"

    def get_queryset(self) -> QuerySet[Any]:
        """Return the restaurants for the current war."""
        queryset = models.War.get().menus.all()
        return queryset


class VoteView(View, employee_utils.EmployeeRequiredMixin):
    """View for voting on a menu."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Return the vote page."""
        menu = models.Menu.objects.get(pk=pk)
        if not menu:
            return redirect("wars:participants")

        if not menu.wars.filter(pk=models.War.get().pk).exists():
            return redirect("wars:participants")

        if menu.votes.filter(employee=self.request.user.employee).exists():
            return redirect("wars:participants")

        menu.votes.create(employee=self.request.user.employee, war=models.War.get())
        return redirect("wars:participants")


class UnvoteView(View, employee_utils.EmployeeRequiredMixin):
    """View for unvoting on a menu."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Return the vote page."""
        menu = models.Menu.objects.get(pk=pk)
        if not menu:
            return redirect("wars:participants")

        if not menu.wars.filter(pk=models.War.get().pk).exists():
            return redirect("wars:participants")

        if not menu.votes.filter(employee=self.request.user.employee).exists():
            return redirect("wars:participants")

        menu.votes.filter(employee=self.request.user.employee).delete()
        return redirect("wars:participants")


class LeaderboardView(ListView):
    """View for showing the leaderboard."""

    model = models.Menu
    template_name = "wars/leaderboard.html"
    context_object_name = "menus"

    def get_queryset(self) -> QuerySet[Any]:
        """Return the menus for the current war."""
        queryset = super().get_queryset()
        return queryset.filter(wars=models.War.get())
