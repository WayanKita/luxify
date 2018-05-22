from .models import Participant
from django import forms


# Form for participants, used by ParticipantFormView, to create registration_form.html
class ParticipantForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # hides password field

    class Meta:
        model = Participant
        fields = "__all__"
