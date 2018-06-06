from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError


from floorPlan.form import ParticipantForm, UserForm
from .models import *
from survey.models import Survey, Question


# Function to check whether a Participant with email matches a Participant in the database
def participant_authentication_check(email):
    try:
        participant = Participant.objects.get(email=email)
    except:
        return False
    if participant.email == email:
        return True
    else:
        return False


# Function to check whether a Participant with email is logged in
def participant_login_check(email):
    try:
        participant = Participant.objects.get(email=email)
    except:
        return False
    if participant.logged_in:
        return True
    else:
        return False


# Serializes a Room object to/from JSON
class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'
        # select all fields from Room model
        # exclude = ()                                              # select all fields except ()
        # fields = ['name', 'size']                                 # select name and size fields


# Serializes a ParticipantForm object to/from JSON
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get("username", None)
        if User.objects.filter(username=username).exists():
            raise ValidationError("This email already exists")
        else:
            return data


# Serializes a Sensor object to/from JSON
class SensorTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor_Table
        fields = '__all__'


# Serializes a Sensor object to/from JSON
class SensorUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor_User
        fields = '__all__'


# Serializes a Table object to/from JSON
class DeskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Desk
        fields = '__all__'


# Serializes a Window object to/from JSON
class WindowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Window
        fields = '__all__'


# Serializes a Window object to/from JSON
class DoorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Door
        fields = '__all__'


# Serializes a Chair object to/from JSON
class ChairSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chair
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    chair = ChairSerializer(many=True, read_only=True)

    class Meta:
        model = Desk
        fields = ('room', 'number', 'pos_x', 'pos_y', 'length_x', 'length_y', 'illuminance', 'chair')


class RoomGeneratorSerializer(serializers.ModelSerializer):
    # room = RoomSerializer(many=True, read_only=True)
    desk = TableSerializer(many=True, read_only=True)
    window = WindowSerializer(many=True, read_only=True)
    chair = ChairSerializer(many=True, read_only=True)
    door = DoorSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ("room_name", "x_length", "y_length", "desk", "window", "chair", "door")


# Serializes a Participant object to/from JSON
class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = "__all__"


# Serializes a Survey object to/from JSON
class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = "__all__"


# Serializes a Question object to/from JSON
class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class ParticipantRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantRequest
        fields = ('email', 'request_type')


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = '__all__'


# Validates a Participant object sent by Android application
class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    # Overwrites is_valid function from Django
    def validate(self, data):
        # get email and password from POST body
        email = data.get("email", None)
        password = data.get("password", None)
        # Try to find a Participant with matching email from POST body else raise ValidationError
        try:
            user = Participant.objects.get(email=email)
            raise ValidationError("User: " + email + " already exists")
        except:
            user = User()
            user.email = email
            user.set_password(password)                              # changes the log in state of Participant to True
            user.save()  # saves changes made to Participant on the database
        return data


# Validates a Participant object sent by Android application
class ParticipantToggleWorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParticipantWorkspace
        fields = "__all__"

    # Overwrites is_valid function from Django
    def validate(self, data):
        # get email and password from POST body
        email = data.get("email", None)
        participant = User.objects.get(username=email)
        participant.email = participant.email
        participant.in_workspace = data.get("in_workspace", None)
        participant.room = data.get("room", None)
        participant.save()
        return data


# Validate that Participant making a request is logged in
class AuthenticateParticipant(serializers.ModelSerializer):

    class Meta:
        model = ParticipantRequest
        fields = "__all__"

    # Overwrite default authentication for Participant
    def validate(self, data):
        email = data.get("email", None)
        if not participant_authentication_check(email):
            raise ValidationError("User: "+email+" does not exist")
        if not participant_login_check(email):
            raise ValidationError("User "+email+" is not logged in")
        return data


# Validate that Participant making a request is logged in
class AuthenticateUser(serializers.ModelSerializer):

    class Meta:
        model = UserRequest
        fields = "__all__"

    # Overwrite default authentication for Participant
    def validate(self, data):
        email = data.get("email", None)
        token = data.get("CSRFTOKEN", None)
        return data




# Validate that Participant making a request is logged in
class AlertnessQuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlertnessQuestionnaire
        fields = "__all__"

    # Overwrite default authentication for Participant
    def validate(self, data):
        email = data.get("email", None)
        if not participant_authentication_check(email):
            raise ValidationError("User: " + email + " does not exist")
        if not participant_login_check(email):
            raise ValidationError("User " + email + " is not logged in")
        return data


# Validate that Participant making a request is logged in
class DemographicQuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemographicQuestionnaire
        fields = "__all__"

    # Overwrite default authentication for Participant
    def validate(self, data):
        email = data.get("email", None)
        if not participant_authentication_check(email):
            raise ValidationError("User: " + email + " does not exist")
        if not participant_login_check(email):
            raise ValidationError("User " + email + " is not logged in")
        return data


class AlertnessQuestionnairePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAlertnessRequest
        fields = '__all__'


class DemographicQuestionnairePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostDemographicRequest
        fields = '__all__'


class ParticipantInWorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantWorkspace
        fields = '__all__'


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAnalyticRequest
        fields = '__all__'

        # Overwrite default authentication for Participant
        def validate(self, data):
            email = data.get("email", None)
            if not participant_authentication_check(email):
                raise ValidationError("User: " + email + " does not exist")
            if not participant_login_check(email):
                raise ValidationError("User " + email + " is not logged in")
            return data
