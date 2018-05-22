from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError


from floorPlan.form import ParticipantForm
from .models import *


def user_authentication_check(email):
    try:
        user = Participant.objects.get(email=email)
    except:
        return False
    if user.email == email:
        return True
    else:
        return False


def user_login_check(email):
    try:
        user = Participant.objects.get(email=email)
    except:
        return False
    if user.email == email:
        return True
    else:
        return False


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        # field = ('code', 'x_length', 'y_length')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParticipantForm
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = '__all__'


class WindowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Window
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
        try:
            user = Participant.objects.get(email=email)
        except:
            raise ValidationError("user does not exist, empty")
        if not user.email == email:
            raise ValidationError("user does not exist")
        if not user.password == password:
            raise ValidationError("This password is WRONG")
        user.loggedIn = True
        user.save()
        return data


class AuthenticateUser(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = "__all__"

    def validate(self, data):
        email = data.get("email", None)
        if not user_authentication_check(email):
            raise ValidationError("User: "+email+" does not exist")
        if not user_login_check(email):
            raise ValidationError("User "+email+" is not logged in")
        return data




