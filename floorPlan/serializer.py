from rest_framework import serializers
from .models import Room
from .form import UserForm


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        # field = ('code', 'x_length', 'y_length')
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserForm
        fields = '__all__'
