from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .form import ParticipantForm
from .models import *
from .serializer import *

# INDEX PAGE
# Defines presentation of the index page /floorPlan
def index(request):
    all_rooms = Room.objects.all()
    template = loader.get_template('floorPlan/floorPlan.html')
    context = {
        'all_rooms': all_rooms,
    }
    return HttpResponse(template.render(context, request))


# CREATE VIEWS
# Defines the fields for the Room form on room_form.html
class RoomCreate(CreateView):
    model = Room
    fields = ["room_name", "x_length", "y_length"]


# Defines the fields for the Table form on desk_form.html
class DeskCreate(CreateView):
    model = Desk
    fields = ['room', 'number', 'pos_x', 'pos_y', 'length_x', 'length_y', 'illuminance']


# Defines the fields for the Chair form on chair_form.html
class ChairCreate(CreateView):
    model = Chair
    fields = ['desk', 'side', 'occupied']


# Defines the fields for the Window form on window_form.html
class WindowCreate(CreateView):
    model = Window
    fields = ['room', 'margin', 'length', 'side']


# Defines the fields for the Sensor form on sensor_form.html
class SensorCreate(CreateView):
    model = Sensor
    fields = ['name', 'date', 'value']


# DETAILED VIEWS
# Defines the detailed view of a Room on room_detail.html
class DetailView(generic.DetailView):
    model = Room
    template_name = 'floorPlan/room_detail.html'


# DELETE VIEWS
# Defines the delete view of a Room on room_detail.html
class RoomDelete(DeleteView):
    model = Room
    success_url = reverse_lazy('floorPlan:index')


class ParticipantFormView(View):
    form_class = ParticipantForm
    template_name = 'floorPlan/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.save()

            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('floorPlan:index')

        return render(request, self.template_name, {'form': form})


# API VIEWS
# Title : Get registered Participants | Register Participants.
# URL : /floorPlan/android_add_user
# Method : GET | POST
# Data Params : [{ email : [string], password : [string]}]
# Response Codes: Success (201 CREATED), Bad Request (400)
class RegisterAPI(APIView):
    form_class = ParticipantForm

    def get(self, request):
        user = User.objects.all()
        serializer = ParticipantSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParticipantForm(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Log in Participants.
# URL : /floorPlan/android_login
# Method : POST
# Data Params : [{ email : [string], password : [string]}]
# Response Codes: Success (200 CREATED), Bad Request (400), Internal Server Error (500)
class LoginAPI(APIView):
    serializer_class = ParticipantLoginSerializer

    def post(self, request):
        serializer = ParticipantLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Defines the API view to GET sensors' information
class SensorAPI(APIView):
    serializer_class = AuthenticateUser

    def post(self, request):
        serializer = AuthenticateUser(data=request.data)
        if serializer.is_valid():
            return Response(SensorSerializer(Sensor.objects.all(), many=True).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Defines the API view to GET desks' information
class TableAPI(APIView):
    serializer_class = AuthenticateUser

    def post(self, request):
        serializer = AuthenticateUser(data=request.data)
        if serializer.is_valid():
            return Response(DeskSerializer(Desk.objects.all(), many=True).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Defines the API view to GET windows' information
class WindowAPI(APIView):
    serializer_class = AuthenticateUser

    def post(self, request):
        serializer = AuthenticateUser(data=request.data)
        if serializer.is_valid():
            return Response(WindowSerializer(Window.objects.all(), many=True).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Defines the API view to GET rooms' information
class RoomAPI(APIView):
    serializer_class = AuthenticateUser

    def post(self, request):
        serializer = AuthenticateUser(data=request.data)
        if serializer.is_valid():
            return Response(RoomSerializer(Room.objects.all(), many=True).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomGeneratorAPI(APIView):
    serializer_class = ParticipantRequestSerializer

    def post(self, request):
        serializer = AuthenticateUser(data=request.data)
        if serializer.is_valid():
            if request.data.get('request_type') == 'rooms':
                return Response(RoomSerializer(Room.objects.all(), many=True).data, status=status.HTTP_200_OK)
            else:
                room = Room.objects.filter(pk=request.data.get('request_type'))
                return Response(RoomGeneratorSerializer(room, many=True, label="room").data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









