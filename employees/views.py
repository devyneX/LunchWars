"""Employee views."""
from datetime import timedelta

from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.shortcuts import render
from django.db import models
from wars import models as war_models


# Create your views here.
class IndexView(View):
    """Index view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request."""
        return redirect("accounts:login")


class EmployeeDashboardView(TemplateView):
    """Employee dashboard view."""

    template_name = "employees/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employee"] = self.request.user.employee
        # get yesterday's winner
        # context["lunch"] =
        return context


class TodaysLunchView(View):
    """Today's lunch view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request."""
        yesterday = timezone.now() - timedelta(days=1)
        menu = (
            war_models.War.objects.filter(date=yesterday)
            .first()
            .menus.all()
            .annotate(num_votes=models.Count("votes"))
            .order_by("-num_votes")
            .first()
        )

        if menu is None:
            return redirect("employees:dashboard")

        return render(request, "employees/lunch.html", {"menu": menu})
