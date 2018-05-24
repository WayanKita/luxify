from rest_framework.exceptions import ValidationError

from floorPlan import models
from .models import Participant
from django import forms


# Form for participants, used by ParticipantFormView, to create registration_form.html
class ParticipantForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # hides password field

    class Meta:
        model = Participant
        fields = ['email', 'password']
        # fields = '__all__'
    # def validate(self, data):
    #     print("lol")
    #     if Participant.objects.filter(email=self.email).exists():
    #         raise ValidationError('Name must be unique per site')
