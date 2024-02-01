from django import forms

from restaurants import models as restaurant_models


class AddToMenuForm(forms.ModelForm):
    selected = forms.BooleanField(required=False)

    class Meta:
        model = restaurant_models.Dish
        fields = []
