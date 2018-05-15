from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        #field = ('code', 'x_length', 'y_length')
        fields = '__all__'
