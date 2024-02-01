"""Utils for the employees app."""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class EmployeeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin for employee required views."""

    def test_func(self):
        """Check if the user is an employee."""
        return self.request.user.is_employee
