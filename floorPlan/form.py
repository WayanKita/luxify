from rest_framework.exceptions import ValidationError

from floorPlan import models
from .models import Participant
from django import forms
from django.contrib.auth.models import User


# Form for participants, used by ParticipantFormView, to create registration_form.html
class ParticipantForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # hides password field

    class Meta:
        model = Participant
        fields = ['email', 'password']
        # fields = '__all__'

    def validate(self, data):
        if Participant.objects.filter(email=self.email).exists():
            raise ValidationError('Name must be unique per site')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']