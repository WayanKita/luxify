import csv
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .form import *
from .models import *
from .serializer import *


# from survey.models import *


# INDEX PAGE
# Defines presentation of the index page /floorPlan
def room_plan(request):
    all_rooms = Room.objects.all()
    return render(request,
                  'floorPlan/floorPlan.html',
                  {'all_rooms': all_rooms})


# Defines presentation of the index page /API
@login_required
@staff_member_required
def home(request):
    all_rooms = Room.objects.all()
    return render(request,
                  'floorPlan/home.html',
                  {'all_rooms': all_rooms})


def alertness_questionnaire(request):
    all_questionnaire = AlertnessQuestionnaire.objects.all()
    return render(request,
                  'floorPlan/alertness_questionnaire.html',
                  {'all_questionnaire': all_questionnaire})


def demographic_questionnaire(request):
    all_questionnaire = DemographicQuestionnaire.objects.all()
    return render(request,
                  'floorPlan/demographic_questionnaire.html',
                  {'all_questionnaire': all_questionnaire})


def user(request):
    all_participant = Participant.objects.all()
    all_room = Room.objects.all()
    return render(request,
                  'floorPlan/user.html',
                  {'all_participant': all_participant,
                   'all_room:': all_room})


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
    model = Sensor_Table
    fields = ['desk', 'time_stamp', 'light_value', 'occupancy_value']


# DETAILED VIEWS
# Defines the detailed view of a Room on room_detail.html
class DetailView(generic.DetailView):
    model = Room
    template_name = 'floorPlan/room_detail.html'


# Defines the detailed view of a Room on room_detail.html
# class AlertnessQuestionnaireView(generic.DetailView):
#     model = AlertnessQuestionnaire
#     template_name = 'floorPlan/alertness_questionnaire.html'


# DELETE VIEWS
# Defines the delete view of a Room on room_detail.html
class RoomDelete(DeleteView):
    model = Room
    success_url = reverse_lazy('floorPlan:room-plan')


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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('floorPlan:index')

        return render(request, self.template_name, {'form': form})


# API VIEWS
# Title : Get registered Participants | Register Participants.
# URL : /API/add_user
# URL : luxify/API/add_user
# Method : GET | POST
# Data Params : [{ username : [string], password : [string]}]
# Response Codes: Success (201 CREATED), Bad Request (400),
class RegisterAPI(APIView):
    form_class = ParticipantForm

    def get(self, request):
        participant = Participant.objects.all()
        serializer = ParticipantSerializer(participant, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParticipantForm(data=request.data)
        if serializer.is_valid():
            serializer.save()
            participant = Participant.objects.get(username=request.data.get('username'))
            participant.logged_in = True
            participant.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get sensor information.
# URL : /API/sensor
# Title : Log in Participants.
# URL : luxify/API/login
# Method : POST
# Data Params : [{ username : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class SensorTableAPI(APIView):
    serializer_class = AuthenticateParticipant
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        if int(pk) > 0:
            if Sensor_Table.objects.filter(pk=pk).count() > 0:
                return Response(SensorTableSerializer(Sensor_Table.objects.filter(pk=pk), many=True).data,
                                status=status.HTTP_200_OK)
            return Response("Sensor table " + pk + " not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(SensorTableSerializer(Sensor_Table.objects.all(), many=True).data,
                            status=status.HTTP_200_OK)


# Title : Get sensor information.
# URL : /API/sensor
# URL : luxify/API/sensor
# Method : POST
# Data Params : [{ username : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class SensorUserAPI(APIView):
    serializer_class = AuthenticateParticipant
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        if int(pk) > 0:
            if Sensor_User.objects.filter(pk=pk).count() > 0:
                return Response(SensorUserSerializer(Sensor_User.objects.filter(pk=pk), many=True).data,
                                status=status.HTTP_200_OK)
            return Response("Sensor user " + pk + " not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(SensorUserSerializer(Sensor_User.objects.all(), many=True).data,
                            status=status.HTTP_200_OK)


# Title : Get table information.
# URL : None
# Method : POST
# Data Params : [{ username : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class DeskAPI(APIView):
    serializer_class = AuthenticateParticipant
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        if int(pk) > 0:
            if Desk.objects.filter(pk=pk).count() > 0:
                return Response(DeskSerializer(Desk.objects.filter(pk=pk), many=True).data,
                                status=status.HTTP_200_OK)
            return Response("Desk " + pk + " not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(DeskSerializer(Desk.objects.all(), many=True).data,
                            status=status.HTTP_200_OK)


# Title : Get window information.
# URL : /API/window
# URL : luxify/API/window
# Method : POST
# Data Params : [{ username : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class WindowAPI(APIView):
    serializer_class = AuthenticateParticipant
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        if int(pk) > 0:
            if Window.objects.filter(pk=pk).count() > 0:
                return Response(WindowSerializer(Window.objects.filter(pk=pk), many=True).data,
                                status=status.HTTP_200_OK)
            return Response("Window " + pk + " not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(WindowSerializer(Window.objects.all(), many=True).data,
                            status=status.HTTP_200_OK)


# Title : Get room information.
# URL : /API/room
# Method : GET
# Data Params :
# Response Codes: Success (200 OK), Internal Server Error (500)
# URL : luxify/API/room
# Method : POST
# Data Params : [{ username : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class RoomAPI(APIView):
    serializer_class = AuthenticateParticipant
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        if int(pk) > 0:
            if Room.objects.filter(pk=pk).count() > 0:
                return Response(RoomSerializer(Room.objects.filter(pk=pk), many=True).data,
                                status=status.HTTP_200_OK)
            return Response("Room " + pk + " not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(RoomSerializer(Room.objects.all(), many=True).data,
                            status=status.HTTP_200_OK)


# Title : Get a bundled room plan (with table(with chair), windows and doors) information.
# URL : /API/room_generator
# URL : luxify/API/room_generator
# Method : POST
# Data Params : [{ username : [string], room_type : [rooms] | [int(1+)]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class RoomGeneratorAPI(APIView):
    serializer_class = ParticipantRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        if int(pk) > 0:
            if Room.objects.filter(pk=pk).count() > 0:
                return Response(RoomGeneratorSerializer(Room.objects.filter(pk=pk), many=True, label="room").data,
                                status=status.HTTP_200_OK)
            return Response("Room " + pk + " not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(RoomSerializer(Room.objects.all(), many=True).data, status=status.HTTP_200_OK)


# Title : Get a bundled room plan (with table(with chair), windows and doors) information.
# URL : /API/room_generator
# URL : luxify/API/room_generator
# Method : POST
# Data Params : [{ username : [string], room_type : [rooms] | [int(1+)]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class RecommendDeskAPI(APIView):
    serializer_class = ParticipantRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
            if Room.objects.filter(pk=pk).count() > 0:
                desks = Desk.objects.filter(room=Room.objects.filter(pk=pk))
                for desk in desks:
                    desk.illuminance
                return Response(RoomGeneratorSerializer(Room.objects.filter(pk=pk), many=True, label="room").data,
                                status=status.HTTP_200_OK)
            return Response("Room " + pk + " not found", status=status.HTTP_404_NOT_FOUND)


# Title : Receive alertness questionnaire answer.
# URL : /API/alertness_questionnaire
# URL : luxify/API/alertness_questionnaire
# Method : POST
# Data Params : [{ username : [string], time_stamp : [YYYY-MM-DDTHH:MM], answer : int[1-10]}]
# Response Codes: Success (201 CREATED), Bad Request (400), Internal Server Error (500)
class AlertnessQuestionnaireAPI(APIView):
    serializer_class = AlertnessQuestionnairePostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = AuthenticateUser(data=request.data)
        if serializer.is_valid():
            alert_answer = AlertnessQuestionnaire()
            participant = User.objects.get(username=request.data.get("username"))
            alert_answer.username = participant.participant
            alert_answer.time_stamp = request.data.get('time_stamp')
            alert_answer.answer = request.data.get('answer')
            alert_answer.save()
            return Response(AlertnessQuestionnaireSerializer(alert_answer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Receive alertness questionnaire answer.
# URL : /API/alertness_questionnaire
# URL : luxify/API/alertness_questionnaire
# Method : POST
# Data Params : [{ username : [string], time_stamp : [YYYY-MM-DDTHH:MM], answer : [comma separated string]]
# Response Codes: Success (201 CREATED), Bad Request (400), Internal Server Error (500)
class DemographicQuestionnaireAPI(APIView):
    serializer_class = DemographicQuestionnairePostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        survey = Question.objects.all()
        serializer = QuestionSerializer(survey, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthenticateUser(data=request.data)
        if serializer.is_valid():
            demographic_answer = DemographicQuestionnaire()
            participant = User.objects.get(username=request.data.get("username"))
            demographic_answer.username = participant.participant
            demographic_answer.time_stamp = request.data.get('time_stamp')
            demographic_answer.answer = request.data.get('answer')
            demographic_answer.save()
            user = User.objects.get(username=request.data.get("username"))
            demographic_answer.username = user.participant
            try:
                profile_table = ParticipantProfiles.objects.get(answer=request.data.get("answer"))
                user.participant.profile = profile_table.profile
            except:
                count = ParticipantProfiles.objects.all().count()
                user.participant.profile = count + 1
                new_profile = ParticipantProfiles()
                new_profile.answer = request.data.get('answer')
                new_profile.profile = count + 1
                user.save()
                new_profile.save()
            return Response(DemographicQuestionnaireSerializer(demographic_answer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get a bundled room plan (with table(with chair), windows and doors) information.
# URL : /API/workspace
# URL : luxify/API/room_generator
# Method : POST
# Data Params : [{ username : [string], room_type : [rooms] | [int(1+)]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class WorkspaceAPI(APIView):
    serializer_class = ParticipantInWorkSpaceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ParticipantToggleWorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get a bundled room plan (with table(with chair), windows and doors) information.
# URL : /API/questionnaire_check
# URL : luxify/API/room_generator
# Method : POST
# Data Params : [{ username : [string], room_type : [rooms] | [int(1+)]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class QuestionnaireCheckAPI(APIView):
    serializer_class = UserRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, key):
        if int(key) == 0:
            participant = User.objects.get(username=request.data.get('username')).participant
            return Response(ParticipantSerializer(participant).data, status=status.HTTP_200_OK)
        else:
            if User.objects.get(username=request.data.get('username')).count() > 0:
                participant = User.objects.get(username=request.data.get('username')).participant
                participant.survey_done = True
                participant.save()
                return Response(ParticipantSerializer(participant).data, status=status.HTTP_200_OK)
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)


# Title : Receive analytics from the application
# URL : luxify/API/analytic
# Method : POST
# Data Params : [{ username : [string], time_stamp : [datetime], event : [string] }]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class AnalyticsAPI(APIView):
    serializer_class = AnalyticsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            analytics = Analytics()
            analytics.username = Participant.objects.get(username=request.data.get("username"))
            analytics.time_stamp = request.data.get('time_stamp')
            analytics.event = request.data.get('event')
            analytics.save()
            serializer = AnalyticsSerializer(analytics)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# SURVEY MODELS


# SECURE USER


# API VIEWS
# Title : Get registered Participants | Register Participants.
# URL : /API/register
# Method : GET | POST
# Data Params : [{ username : [string], password : [string]}]
# Response Codes: Success (201 CREATED), Bad Request (400),
class RegisterUserAPI(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get("username")
            password = request.data.get("password")
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.save()
            participant = Participant()
            participant.username = User.objects.get(username=username)
            participant.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LOGIN
class Login(CreateView):
    model = User
    fields = ['username', 'password']
