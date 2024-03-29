"""Authentication views."""
from django.contrib.auth import login
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from . import models
from . import forms
from restaurants import models as restaurant_models


class SignUpView(FormView):
    """Sign up view."""

    template_name = "accounts/signup.html"
    form_class = forms.SignUpForm

    def form_valid(self, form: forms.SignUpForm) -> HttpResponse:
        """If the form is valid, save the associated model."""
        user = form.save(commit=True)
        if form.cleaned_data["user_type"] == "employee":
            models.Employee.objects.create(user=user)
            user.is_employee = True
            user.save()

        elif form.cleaned_data["user_type"] == "restaurant_representative":
            models.RestaurantRepresentative.objects.create(user=user)
            user.is_restaurant_representative = True
            user.save()

        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Return success url."""
        if self.request.user.is_employee:
            return reverse_lazy("employees:dashboard")

        if self.request.user.is_restaurant_representative:
            return reverse_lazy("restaurants:create")

        return reverse_lazy("accounts:login")


class Login(LoginView):
    """Login view."""

    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        """Return success url."""

        if self.request.user.is_employee:
            return reverse_lazy("employees:dashboard")

        if self.request.user.is_restaurant_representative:
            if restaurant_models.Restaurant.objects.filter(
                restaurant_representative=self.request.user.restaurant_representative
            ).exists():
                return reverse_lazy("restaurants:dashboard")
            else:
                return reverse_lazy("restaurants:create")

        return super().get_success_url()
