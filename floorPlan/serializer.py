from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError

from floorPlan.form import WayanForm
from .models import Room, Wayan


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        # field = ('code', 'x_length', 'y_length')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = WayanForm
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

class WayanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wayan
        fields = "__all__"


class WayanLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wayan
        fields = "__all__"

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = Wayan.objects.get(email=email)
        if not user.email == email:
            raise ValidationError("user does not exist")
        if not user.password == password:
            raise ValidationError("This password is WRONG")
        user.loggedIn = True
        user.save()
        return data



