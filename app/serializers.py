from django.contrib.auth.models import User
from rest_framework import serializers
from app.models.room import Desk, Door, Window, Room
from app.models.questionnaire import Questionnaire, Question, Choice
from app.models.preference import AlertnessInterval
from app.models.participant import \
    Category, Participant, QuestionnaireAnswer, \
    AlertnessQuestionnaireAnswer, Analytics


"""
Serializers
"""


class DeskSerializer(serializers.ModelSerializer):

    """
    Desk serializer
    """

    class Meta:
        model = Desk
        fields = '__all__'
        extra_kwargs = {
            'side': {'read_only': True}, 'pos_x': {'read_only': True}, 'pos_y': {'read_only': True},
            'illuminance': {'read_only': True}, 'room': {'read_only': True},
            'illuminance_sensor': {'read_only': True}, 'occupancy_sensor': {'read_only': True},
        }  # defines that these fields can only be read


class DoorSerializer(serializers.ModelSerializer):

    """
    Door serializer
    """

    class Meta:
        model = Door
        fields = '__all__'


class WindowSerializer(serializers.ModelSerializer):

    """
    Window serializer
    """

    class Meta:
        model = Window
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    """
    Room serializer
    """

    desk = DeskSerializer(many=True)  # include the desks in the room
    door = DoorSerializer(many=True)  # include the doors in the room
    window = WindowSerializer(many=True)  # include the windows in the room

    class Meta:
        model = Room
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    """
    Category serializer
    """

    class Meta:
        model = Category
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):

    """
    User creation serializer
    """

    class Meta:
        model = User
        fields = ('email', 'password', 'username')  # only inlucde these two fields
        extra_kwargs = {
            'password': {'write_only': True}
        }  # defines fiels that can be written but cannot be viewed

    def create(self, data):

        """
        Creates a new default Django user account
        """

        email = data.get('email')  # set email to the email that was sent
        password = data.get('password')  # set password to the password that was sent
        user = User.objects.create(email=email, username=email)  # create the new user object
        user.set_password(password)  # store the password hash instead of the plain-text password
        user.save()  # save the user account
        return user


class CreateParticipantSerializer(serializers.ModelSerializer):

    """
    Participant creation serializer
    """

    class Meta:
        model = Participant
        exclude = ('user',)  # include all fields except the user field


class ParticipantSerializer(serializers.ModelSerializer):

    """
    Participant serializer
    """

    class Meta:
        model = Participant
        exclude = ('user', 'profile')  # exclude user and profile from the fields that are returned
        extra_kwargs = {
            'category': {'read_only': True}
        }  # defines that category can only be read


class ChoiceSerializer(serializers.ModelSerializer):

    """
    Choice serializer
    """

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    """
    Question serializer
    """

    question_choice = ChoiceSerializer(many=True)  # include answer choices for this question

    class Meta:
        model = Question
        fields = '__all__'


class QuestionnaireSerializer(serializers.ModelSerializer):

    """
    Questionnaire serializer
    """

    questionnaire_question = QuestionSerializer(many=True)  # include questions for this questionnaire

    class Meta:
        model = Questionnaire
        fields = '__all__'


class QuestionnaireAnswerSerializer(serializers.ModelSerializer):

    """
    QuestionnaireAnswer serializer
    """

    class Meta:
        model = QuestionnaireAnswer
        fields = '__all__'


class AnalyticsSerializer(serializers.ModelSerializer):

    """
    Analytics serializer
    """

    class Meta:
        model = Analytics
        fields = '__all__'


class AlertnessQuestionnaireAnswerSerializer(serializers.ModelSerializer):

    """
    AlertnessQuestionnaireAnswer serializer
    """

    class Meta:
        model = AlertnessQuestionnaireAnswer
        fields = '__all__'
        extra_kwargs = {
            'illuminance': {'read_only': True},
        }  # defines that illuminance can only be read


class AlertnessIntervalSerializer(serializers.ModelSerializer):

    """
    AlertnessInterval serializer
    """

    class Meta:
        model = AlertnessInterval
        fields = '__all__'
