from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError

from floor_plan.form import ParticipantForm
from .models import Room, Participant


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        # field = ('code', 'x_length', 'y_length')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParticipantForm
        fields = '__all__'


# class UserAndroidSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         email = serializers.EmailField()
#
#     def validate_username(self, email):
#         username = data.get("username", None)
#         user = User.objects.filter(username=username)
#         #if user.exists():
#         if User.objects.filter(username=username).exists():
#             raise ValidationError("This email already exists")
#         else:
#             return email

class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = "__all__"


class ParticipantLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = "__all__"

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = Participant.objects.get(email=email)
        if not user.email == email:
            raise ValidationError("user does not exist")
        if not user.password == password:
            raise ValidationError("This password is WRONG")
        user.loggedIn = True
        user.save()
        return data



