import csv
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
import logging
from .form import *
from .serializer import *


logger = logging.getLogger(__name__)

# TODO: change all bad POST requests
# TODO: remove all views linked to website luxify
# TODO: add comments to code
# TODO: remove API views of API and ensure that this did not affect correctness of API
# (look into necessity of serializers)


def do_download(model, all_objects):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format('test')
    writer = csv.writer(response)

    fields = [field for field in model.get_fields() if not field.many_to_many and not field.one_to_many]
   
    writer.writerow([field.name for field in fields])
   
    for desk in all_objects:
        row = []
        for field in fields:
            field_value = getattr(desk, field.name)
            row.append(field_value)

        writer.writerow(row)
    return response


def room_plan(request):
    all_rooms = Room.objects.all()
    return render(request,
                  'floorPlan/floorPlan.html',
                  {'all_rooms': all_rooms})


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


def analytics(request):
    all_analytics = Analytics.objects.all()
    return render(request,
                  'floorPlan/analytics.html',
                  {'all_analytics': all_analytics})


def user_category(request):
    all_user_category = UserCategory.objects.all()
    all_layout = Layout.objects.all()
    return render(request,
                  'floorPlan/user_category_setting.html',
                  {'all_user_category': all_user_category,
                   'all_layout': all_layout})


def alertness(request):
    all_user_category = UserCategory.objects.all()
    return render(request,
                  'floorPlan/user_category_setting.html',
                  {'all_user_category': all_user_category})


def send_file(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format('test')
    writer = csv.writer(response)
    model = Desk._meta

    fields = [field for field in model.get_fields() if not field.many_to_many and not field.one_to_many and not field.is_relation]
   
    writer.writerow([field.name for field in fields])
   
    for desk in Desk.objects.all():
        row = []
        for field in fields:
            field_value = getattr(desk, field.name)
            row.append(field_value)

        writer.writerow(row)
    return response


class QuestionnaireCreate(CreateView):
    model = Survey
    fields = ['name', 'description']


class DemographicCreate(CreateView):
    model = Question
    fields = ['text', 'order', 'survey', 'type', 'choices']


class RoomCreate(CreateView):
    model = Room
    fields = ["room_name"]


class DeskCreate(CreateView):
    model = Desk
    fields = ['room', 'number', 'pos_x', 'pos_y', 'length_x', 'length_y', 'chair_side']


class WindowCreate(CreateView):
    model = Window
    fields = ['room', 'margin', 'length', 'side']


class SensorCreate(CreateView):
    model = SensorHistory
    fields = ['desk', 'time_stamp', 'light_value', 'occupancy_value']


class DetailView(generic.DetailView):
    model = Room
    template_name = 'floorPlan/room_detail.html'


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


class RegisterAPI(APIView):
    form_class = ParticipantForm

    def get(self, request):
        participant = Participant.objects.all()
        serializer = ParticipantSerializer(participant, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParticipantForm(data=request.data)
        if serializer.is_valid():

            participant = Participant.objects.get(username=request.data.get('username'))
            if Participant.objects.latest('user_category').user_category() == 0:
                participant.user_category = 1
            else:
                participant.user_category = 2
            participant.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# class SensorTableAPI(APIView):
#     serializer_class = AuthenticateParticipant
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request, pk):
#         if int(pk) > 0:
#             if SensorHistory.objects.filter(pk=pk).count() > 0:
#                 return Response(SensorTableSerializer(SensorHistory.objects.filter(pk=pk), many=True).data,
#                                 status=status.HTTP_200_OK)
#             return Response("Sensor table " + pk + " not found", status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response(SensorTableSerializer(SensorHistory.objects.all(), many=True).data,
#                             status=status.HTTP_200_OK)


class UserNameAPI(APIView):
    serializer_class = ParticipantSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user):
        try:
            participant = Participant.objects.get(username=User.objects.get(username=user))
            participant.name = request.data.get("name")
            participant.save()
            return Response("Name"+request.data.get("name")+" has been set",
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)


class AlertnessIntervalAPI(APIView):
    serializer_class = AlertnessTimeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        alertness = AlertnessTime.objects.all()
        serializer = AlertnessTimeSerializer(alertness,  many=True)
        return Response(serializer.data)


class UserAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user):
        try:
            return Response(ParticipantSerializer(Participant.objects.filter(username=User.objects.get(username=user)), many=True).data,
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user):
        try:
            participant = Participant.objects.get(username=User.objects.get(username=user))
            participant.desk = request.data.get("desk")
            participant.save()
            return Response("Desk"+request.data.get("desk")+" has been set",
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)


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


class RecommendDeskAPI(APIView):
    serializer_class = ParticipantRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user):
        if User.objects.filter(username=user).count() > 0:
            user_room = User.objects.get(username=user).participant.room
            room = Room.objects.get(pk=user_room)
            desks = Desk.objects.filter(room=room).order_by('-illuminance')
            for desk in desks:
                if desk.occupied:
                    desks = desks.exclude(pk=desk.pk)
            return Response(DeskSerializer(desks, many=True).data,
                            status=status.HTTP_200_OK)
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)


class SetOccupancyAPI(APIView):
    serializer_class = SetOccupancyPostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if Desk.objects.filter(pk=request.data.get("key")).count() > 0:
            desk = Desk.objects.get(pk=request.data.get("key"))
            if int(request.data.get('occupied')) > 0:
                desk.occupied = 1
            else:
                desk.occupied = 0
            desk.save()
            return Response(DeskSerializer(desk).data,
                            status=status.HTTP_200_OK)
        return Response("Desk " + request.data.get("key") + " not found", status=status.HTTP_404_NOT_FOUND)


class UserCategoryAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user):
        try:
            participant = User.objects.get(username=user).participant
            layout = participant.user_category
            user_category = Layout.objects.get(pk=layout)
            return Response(LayoutSerializer(user_category).data,
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("User category for " + user + " not found", status=status.HTTP_404_NOT_FOUND)


class AlertnessQuestionnaireAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = AlertnessQuestionnaireSerializer
        alert_answer = AlertnessQuestionnaire()
        participant = User.objects.get(username=request.data.get("username"))
        alert_answer.username = participant.participant
        alert_answer.time_stamp = request.data.get('time_stamp')
        alert_answer.answer = request.data.get('answer')
        alert_answer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            except ObjectDoesNotExist:
                count = ParticipantProfiles.objects.all().count()
                user.participant.profile = count + 1
                new_profile = ParticipantProfiles()
                new_profile.answer = request.data.get('answer')
                new_profile.profile = count + 1
                user.save()
                new_profile.save()
            return Response(DemographicQuestionnaireSerializer(demographic_answer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspaceAPI(APIView):
    serializer_class = ParticipantInWorkSpaceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ParticipantToggleWorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionnaireCheckAPI(APIView):
    serializer_class = UserRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, key):
        if int(key) == 0:
            participant = User.objects.get(username=request.data.get('username')).participant
            return Response(ParticipantSerializer(participant).data, status=status.HTTP_200_OK)
        else:
            if User.objects.filter(username=request.data.get('username')).count() > 0:
                participant = User.objects.get(username=request.data.get('username')).participant
                participant.survey_done = True
                participant.save()
                return Response(ParticipantSerializer(participant).data, status=status.HTTP_200_OK)
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)


class AnalyticsAPI(APIView):
    serializer_class = AnalyticsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if User.objects.filter(username=request.data.get("username")).count() > 0:
            analytics = Analytics()
            analytics.username = User.objects.get(username=request.data.get("username")).participant
            analytics.time_stamp = request.data.get('time_stamp')
            analytics.event = request.data.get('event')
            analytics.save()
            serializer = AnalyticsSerializer(analytics)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)


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
            try:
                cat = Participant.objects.filter(user_category__gt=0).latest('user_category')
                participant.user_category = (cat.user_category % 3) + 1
            except ObjectDoesNotExist:
                participant.user_category = 1
            participant.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def Download_Alertness_Questionnaire(request):
    return do_download(AlertnessQuestionnaire._meta, AlertnessQuestionnaire.objects.all())


def Download_Analytics(request):
    return do_download(Analytics._meta, Analytics.objects.all())


def Download_Demographic_Questionnaire(request):
    return do_download(DemographicQuestionnaire._meta, DemographicQuestionnaire.objects.all())
