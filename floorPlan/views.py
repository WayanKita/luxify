import csv
import random
from django.http import HttpResponse
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


class UserNameAPI(APIView):
    """
    Changes the name field of a Participant
    """
    serializer_class = ParticipantSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user):
        """
        JSON :param request: name: name of the participant you wish to add (i.e Joe)
        URL :param user: email of the participant you wish to change the name of (i.e example@example.com)
        :return:
            200 OK if request was successful
            401 Unauthorized if request header does not contain BASIC AUTH
            404 NOT FOUND if request was unsuccessful
        """
        try:
            participant = Participant.objects.get(username=User.objects.get(username=user))
            participant.name = request.data.get("name")
            participant.save()
            return Response("Name"+request.data.get("name")+" has been set",
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)


class AlertnessIntervalAPI(APIView):
    """
    Returns the time interval to display the Alertness Questionnaire notification
    """
    serializer_class = AlertnessTimeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        :return:
            200 OK if request was successful
                {
                    id: int
                    interval: int
                }
            401 Unauthorized if request header does not contain BASIC AUTH
        """
        alertness = AlertnessTime.objects.all()
        serializer = AlertnessTimeSerializer(alertness,  many=True)
        return Response(serializer.data)


class UserAPI(APIView):
    """
    Handles User.Participant
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, user):
        """
        Returns all of the Participant's fields with matching email
        :param user: email of the participant's info you want to retrieve
        :return:
        """
        try:
            return Response(ParticipantSerializer(Participant.objects.filter(username=User.objects.get(username=user)), many=True).data,
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user):
        """
        Modify the desk field on Participant
        :param request:
            desk: desk.pk that the user will be sitting at
        :param user: email of the participant's info you want to retrieve
        :return:

        """
        try:
            participant = Participant.objects.get(username=User.objects.get(username=user))
            participant.desk = request.data.get("desk")
            participant.save()
            return Response("Desk"+request.data.get("desk")+" has been set",
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)


class RoomGeneratorAPI(APIView):
    """

    """
    serializer_class = ParticipantRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        """

        :param request:
        :param pk:
        :return:
        """
        if int(pk) > 0:
            if Room.objects.filter(pk=pk).count() > 0:
                return Response(RoomGeneratorSerializer(Room.objects.filter(pk=pk), many=True, label="room").data,
                                status=status.HTTP_200_OK)
            return Response("Room " + pk + " not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(RoomSerializer(Room.objects.all(), many=True).data, status=status.HTTP_200_OK)


class RecommendDeskAPI(APIView):
    """

    """
    serializer_class = ParticipantRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user):
        """

        :param request:
        :param user:
        :return:
        """
        if User.objects.filter(username=user).count() > 0:
            participant = User.objects.get(username=user).participant
            user_room = participant.room
            try:
                formula = Recommendation.objects.get(profile=participant.profile).formula
                formula = formula.replace("^", "**")
                target = eval(formula)
                try:
                    room = Room.objects.get(pk=user_room)
                    desks = Desk.objects.filter(room=room)
                    for desk in desks:
                        if desk.occupied:
                            desks = desks.exclude(pk=desk.pk)
                        else:
                            desk.score = abs(target-desk.illuminance)
                            desk.save()
                    desks = Desk.objects.filter(room=room).order_by('score')
                    return Response(DeskSerializer(desks, many=True).data,
                                    status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    return Response("Room for user not found", status=status.HTTP_404_NOT_FOUND)
            except ObjectDoesNotExist:
                return Response("Recommendation not found", status=status.HTTP_404_NOT_FOUND)
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)


class SetOccupancyAPI(APIView):
    """

    """
    serializer_class = SetOccupancyPostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """

        :param request:
        :return:
        """
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
    """

    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user):
        """

        :param request:
        :param user:
        :return:
        """
        try:
            participant = User.objects.get(username=user).participant
            layout = participant.user_category
            user_category = Layout.objects.get(pk=layout)
            return Response(LayoutSerializer(user_category).data,
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("User category for " + user + " not found", status=status.HTTP_404_NOT_FOUND)


class AlertnessQuestionnaireAPI(APIView):
    """

    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """

        :param request:
        :return:
        """
        serializer = AlertnessQuestionnaireSerializer
        alert_answer = AlertnessQuestionnaire()
        participant = User.objects.get(username=request.data.get("username"))
        alert_answer.username = participant.participant
        alert_answer.time_stamp = request.data.get('time_stamp')
        alert_answer.answer = request.data.get('answer')
        alert_answer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DemographicQuestionnaireAPI(APIView):
    """

    """
    serializer_class = DemographicQuestionnairePostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """

        :param request:
        :return:
        """
        survey = Question.objects.all()
        serializer = QuestionSerializer(survey, many=True)
        return Response(serializer.data)

    def post(self, request):
        """

        :param request:
        :return:
        """
        demographic_answer = DemographicQuestionnaire()
        user = User.objects.get(username=request.data.get("username"))
        demographic_answer.username = user.participant
        demographic_answer.time_stamp = request.data.get('time_stamp')
        demographic_answer.answer = request.data.get('answer')
        demographic_answer.save()
        participant = user.participant
        try:
            profile_table = ParticipantProfiles.objects.get(answer=request.data.get("answer"))
            participant.profile = profile_table.profile
            participant.save()
        except ObjectDoesNotExist:
            count = ParticipantProfiles.objects.all().count()
            participant.profile = count + 1
            new_profile = ParticipantProfiles()
            new_profile.answer = request.data.get('answer')
            new_profile.profile = count + 1
            participant.save()
            new_profile.save()
        return Response(DemographicQuestionnaireSerializer(demographic_answer).data, status=status.HTTP_201_CREATED)


class WorkspaceAPI(APIView):
    """

    """
    serializer_class = ParticipantInWorkSpaceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """

        :param request:
        :return:
        """
        serializer = ParticipantToggleWorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionnaireCheckAPI(APIView):
    """

    """
    serializer_class = UserRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, key):
        """

        :param request:
        :param key:
        :return:
        """
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
    """

    """
    serializer_class = AnalyticsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """

        :param request:
        :return:
        """
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
    """

    """
    serializer_class = UserSerializer

    def post(self, request):
        """

        :param request:
        :return:
        """
        serializer = UserSerializer(data=request.data)
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        participant = Participant()
        participant.username = User.objects.get(username=username)
        participant.user_category = random.randint(1, 3)
        participant.save()
        return Response(ParticipantSerializer(participant).data, status=status.HTTP_201_CREATED)


def download_alertness_questionnaire(request):
    return do_download(AlertnessQuestionnaire._meta, AlertnessQuestionnaire.objects.all())


def download_analytics(request):
    return do_download(Analytics._meta, Analytics.objects.all())


def download_demographic_questionnaire(request):
    return do_download(DemographicQuestionnaire._meta, DemographicQuestionnaire.objects.all())
