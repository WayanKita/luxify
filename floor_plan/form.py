from .models import *
from django import forms


class WayanForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Wayan
        fields = "__all__"
