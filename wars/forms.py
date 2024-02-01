from django import forms

from restaurants import models as restaurant_models
from restaurants import utils as restaurant_utils
from . import models


class ParticipateForm(forms.Form):
    """Form for participating in a war."""

    menu = forms.ModelChoiceField(queryset=models.Menu.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["menu"].queryset = models.Menu.objects.filter(
            restaurant=restaurant_utils.get_restaurant(self.request)
        )


class AddToMenuForm(forms.ModelForm):
    selected = forms.BooleanField(required=False)

    class Meta:
        model = restaurant_models.Dish
        fields = []
