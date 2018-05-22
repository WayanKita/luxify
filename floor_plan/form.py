from .models import *
from django import forms


class ParticipantForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Participant
        fields = "__all__"