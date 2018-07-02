from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *


"""
This file defines the API's of Luxify
"""


def post_response(serializer, response_status):
    if serializer.is_valid(raise_exception=ValueError):
        saved = serializer.save()
        if saved:
            return Response(serializer.data, status=response_status)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomListView(generics.ListAPIView):

    """
    GET:
    Returns a list of rooms, along with any desks, 
    doors, and windows inside the rooms.
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(generics.RetrieveAPIView):

    """
    GET:
    Returns the room with primary key <pk>, 
    along with any desks, doors, and windows inside the room.
    """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class DeskView(APIView):


    """
    GET:
    Returns the desk with primary key <pk>.

    POST:
    Updates the ‘occupied’ field of the desk 
    with primary key <pk>.
    """

    serializer_class = DeskSerializer

    def get(self, request, pk):
        desk = get_object_or_404(Desk, pk=pk)
        serializer = DeskSerializer(desk)
        return Response(serializer.data)

    def post(self, request, pk):
        desk = get_object_or_404(Desk, pk=pk)
        serializer = DeskSerializer(desk, data=request.data)
        return post_response(serializer, status.HTTP_200_OK)


class QuestionnaireView(APIView):

    """
    GET:
    Returns the demographic questionnaire, 
    along with its questions, and answer choices.
    """

    serializer_class = QuestionnaireSerializer

    def get(self, request):
        questionnaire = Questionnaire.objects.latest('id')
        serializer = QuestionnaireSerializer(questionnaire)
        return Response(serializer.data)


class QuestionnaireAnswerView(APIView):

    """
    POST:
    Creates or updates the demographic questionnaire answer 
    of the participant with  an email equal to <email>, 
    depending on whether an answer of that participant already exists.
    """

    serializer_class = QuestionnaireAnswerSerializer

    def post(self, request):
        try:
            questionnaire_answer = QuestionnaireAnswer.objects.get(participant=request.data.get('participant'))
            serializer = QuestionnaireAnswerSerializer(questionnaire_answer, data=request.data)
            return post_response(serializer, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            serializer = QuestionnaireAnswerSerializer(data=request.data)
            return post_response(serializer, status.HTTP_201_CREATED)


class AnalyticsView(APIView):

    """
    POST:
    Creates a new analytics log.
    """

    serializer_class = AnalyticsSerializer

    def post(self, request):
        serializer = AnalyticsSerializer(data=request.data)
        return post_response(serializer, status.HTTP_201_CREATED)


class AlertnessQuestionnaireAnswerView(APIView):

    """
    POST:
    Creates a new alertness questionnaire answer.
    """

    serializer_class = AlertnessQuestionnaireAnswerSerializer

    def post(self, request):
        serializer = AlertnessQuestionnaireAnswerSerializer(data=request.data)
        return post_response(serializer, status.HTTP_201_CREATED)


class CreateParticipantView(APIView):

    """
    POST:
    Creates a new participant.
    """
    
    serializer_class = CreateParticipantSerializer

    def post(self, request):
        user = CreateUserSerializer.create(CreateUserSerializer(), data=request.data)
        participant = Participant.objects.create(user=user)
        serializer = CreateParticipantSerializer(participant, data=request.data)
        return post_response(serializer, status.HTTP_201_CREATED)


class ParticipantView(APIView):

    """
    GET:
    Returns the participant with an email equal to <email>.

    POST:
    Updates the name, room, or desk of a participant with an email equal to <email>.
    """

    serializer_class = ParticipantSerializer

    def get(self, request, username):
        participant = get_object_or_404(Participant, user__username=username)
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data)

    def post(self, request, username):
        participant = get_object_or_404(Participant, user__username=username)
        serializer = ParticipantSerializer(participant, data=request.data)
        return post_response(serializer, status.HTTP_200_OK)


class AlertnessIntervalView(APIView):

    """
    GET:
    Returns the alertness questionnaire interval.
    """

    def get(self, request):
        interval = AlertnessInterval.objects.latest('pk')
        serializer = AlertnessIntervalSerializer(interval)
        return Response(serializer.data)


class RecommendationView(APIView):

    """
    GET:
    Returns an ordered list of desks in the room of the participant with an email equal to <email>. 
    The desks are ordered according to the participant’s personal illuminance recommendation.
    """

    def get(self, request, username):
        participant = get_object_or_404(Participant, user__username=username)
        target_illuminance = participant.recommended_illuminance()
        desks = Desk.recommended_desks(participant.room, target_illuminance)
        serializer = DeskSerializer(desks, many=True)
        return Response(serializer.data)


class CategoryView(APIView):

    """
    GET:
    Returns the category-based layout of the participant with an email equal to <email>.
    """

    serializer_class = CategorySerializer

    def get(self, request, username):
        participant = get_object_or_404(Participant, user__username=username)
        category = participant.category
        serializer = CategorySerializer(category)
        return Response(serializer.data)
