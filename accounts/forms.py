"""Authentication forms"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class SignUpForm(UserCreationForm):
    """Sign up form."""

    user_type = forms.ChoiceField(
        choices=[
            ("employee", "Employee"),
            ("restaurant_representative", "Restaurant Representative"),
        ]
    )

    class Meta:
        """Meta class."""

        model = models.User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "user_type",
        )
        widgets = {
            "user_type": forms.Select(attrs={"required": True}),
        }
