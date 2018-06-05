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
from rest_framework import status
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


# Defines presentation of the index page /floorPlan
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
            participant = Participant.objects.get(email=request.data.get('email'))
            participant.logged_in = True
            participant.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Log in Participants.
# URL : /floorPlan/android_login
# Method : POST
# Data Params : [{ email : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class LoginAPI(APIView):
    serializer_class = ParticipantLoginSerializer

    def post(self, request):
        serializer = ParticipantLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get sensor information.
# URL : /floorPlan/android_sensor
# Method : POST
# Data Params : [{ email : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class SensorAPI(APIView):
    serializer_class = AuthenticateParticipant

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            return Response(SensorSerializer(Sensor_Table.objects.all(), many=True).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get table information.
# URL : None
# Method : POST
# Data Params : [{ email : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class TableAPI(APIView):
    serializer_class = AuthenticateParticipant

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            return Response(DeskSerializer(Desk.objects.all(), many=True).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get window information.
# URL : /floorPlan/android_window
# Method : POST
# Data Params : [{ email : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class WindowAPI(APIView):
    serializer_class = AuthenticateParticipant

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            return Response(WindowSerializer(Window.objects.all(), many=True).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get room information.
# URL : /floorPlan/android_room
# Method : POST
# Data Params : [{ email : [string], password : [string]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class RoomAPI(APIView):
    serializer_class = AuthenticateParticipant

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            return Response(RoomSerializer(Room.objects.all(), many=True).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get a bundled room plan (with table(with chair), windows and doors) information.
# URL : /floorPlan/android_room_generator
# Method : POST
# Data Params : [{ email : [string], room_type : [rooms] | [int(1+)]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class RoomGeneratorAPI(APIView):
    serializer_class = ParticipantRequestSerializer

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            if request.data.get('request_type') == "0":
                return Response(RoomSerializer(Room.objects.all(), many=True).data, status=status.HTTP_200_OK)
            else:
                room = Room.objects.filter(pk=request.data.get('request_type'))
                return Response(RoomGeneratorSerializer(room, many=True, label="room").data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Receive alertness questionnaire answer.
# URL : /floorPlan/android_alertness_questionnaire
# Method : POST
# Data Params : [{ email : [string], time_stamp : [YYYY-MM-DDTHH:MM], answer : int[1-10]}]
# Response Codes: Success (201 CREATED), Bad Request (400), Internal Server Error (500)
class AlertnessQuestionnaireAPI(APIView):
    serializer_class = AlertnessQuestionnairePostSerializer

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            alert_answer = AlertnessQuestionnaire()
            alert_answer.email = Participant.objects.get(email=request.data.get("email"))
            alert_answer.time_stamp = request.data.get('time_stamp')
            alert_answer.answer = request.data.get('answer')
            alert_answer.save()
            return Response(AlertnessQuestionnaireSerializer(alert_answer).data, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Receive alertness questionnaire answer.
# URL : /floorPlan/android_alertness_questionnaire
# Method : POST
# Data Params : [{ email : [string], time_stamp : [YYYY-MM-DDTHH:MM], answer : [comma separated string]]
# Response Codes: Success (201 CREATED), Bad Request (400), Internal Server Error (500)
class DemographicQuestionnaireAPI(APIView):
    serializer_class = DemographicQuestionnairePostSerializer

    def get(self, request):
        survey = Question.objects.all()
        serializer = QuestionSerializer(survey, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            demographic_answer = DemographicQuestionnaire()
            demographic_answer.email = Participant.objects.get(email=request.data.get("email"))
            demographic_answer.time_stamp = request.data.get('time_stamp')
            demographic_answer.answer = request.data.get('answer')
            demographic_answer.save()
            user = Participant.objects.get(email=request.data.get("email"))
            try:
                profile_table = ParticipantProfiles.objects.get(answer=request.data.get("answer"))
                user.profile = profile_table.profile
            except:
                count = ParticipantProfiles.objects.all().count()
                user.profile = count+1
                new_profile = ParticipantProfiles()
                new_profile.answer = request.data.get('answer')
                new_profile.profile = count+1
                user.save()
                new_profile.save()
            return Response(DemographicQuestionnaireSerializer(demographic_answer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get a bundled room plan (with table(with chair), windows and doors) information.
# URL : /floorPlan/android_room_generator
# Method : POST
# Data Params : [{ email : [string], room_type : [rooms] | [int(1+)]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class WorkspaceAPI(APIView):
    serializer_class = ParticipantInWorkSpaceSerializer

    def post(self, request):
        serializer = ParticipantToggleWorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Title : Get a bundled room plan (with table(with chair), windows and doors) information.
# URL : /floorPlan/android_room_generator
# Method : POST
# Data Params : [{ email : [string], room_type : [rooms] | [int(1+)]}]
# Response Codes: Success (200 OK), Bad Request (400), Internal Server Error (500)
class QuestionnaireCheckAPI(APIView):
    serializer_class = ParticipantRequestSerializer

    def post(self, request):
        serializer = AuthenticateParticipant(data=request.data)
        if serializer.is_valid():
            if request.data.get('request_type') == "0":
                participant = Participant.objects.get(email=request.data.get('email'))
                return Response(ParticipantSerializer(participant).data, status=status.HTTP_200_OK)
            if request.data.get('request_type') == "1":
                participant = Participant.objects.get(email=request.data.get('email'))
                participant.survey_done = True
                participant.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# SURVEY MODELS


# SECURE USER


# API VIEWS
# Title : Get registered Participants | Register Participants.
# URL : /floorPlan/android_add_user
# Method : GET | POST
# Data Params : [{ email : [string], password : [string]}]
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
