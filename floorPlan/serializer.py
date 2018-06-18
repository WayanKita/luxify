from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from .models import *
from survey.models import Survey, Question

# TODO: remove API serializers once VIEWS todo have bee completed
# TODO: add comments


def participant_authentication_check(username):
    try:
        participant = Participant.objects.get(username=username)
    except:
        return False
    if participant.username == username:
        return True
    else:
        return False


def participant_login_check(username):
    try:
        participant = Participant.objects.get(username=username)
    except:
        return False
    if participant.logged_in:
        return True
    else:
        return False


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get("username", None)
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username already exists")
        else:
            return data


class SensorTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = SensorHistory
        fields = '__all__'


class DeskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Desk
        fields = '__all__'


class WindowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Window
        fields = '__all__'


class DoorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Door
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Desk
        fields = ('id', 'room', 'number', 'pos_x', 'pos_y', 'length_x', 'length_y', 'illuminance', 'occupied', 'chair_side')


class RoomGeneratorSerializer(serializers.ModelSerializer):
    desk = TableSerializer(many=True, read_only=True)
    window = WindowSerializer(many=True, read_only=True)
    door = DoorSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ("room_name", "desk", "window", "door")


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = "__all__"


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class ParticipantRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantRequest
        fields = ('username', 'request_type')


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        try:
            user = Participant.objects.get(username=username)
            raise ValidationError("User: " + username + " already exists")
        except:
            user = User()
            user.username = username
            user.set_password(password)
            user.save()
        return data


class ParticipantToggleWorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParticipantWorkspace
        fields = "__all__"

    def validate(self, data):
        username = data.get("username", None)
        participant = User.objects.get(username=username).participant
        participant.username = User.objects.get(username=username)
        participant.in_workspace = data.get("in_workspace", None)
        participant.room = data.get("room", None)
        participant.save()
        return data


class AuthenticateUser(serializers.ModelSerializer):

    class Meta:
        model = UserRequest
        fields = "__all__"

    def validate(self, data):
        username = data.get("username", None)
        token = data.get("CSRFTOKEN", None)
        return data


class AlertnessQuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlertnessQuestionnaire
        fields = "__all__"


class DemographicQuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemographicQuestionnaire
        fields = "__all__"

    def validate(self, data):
        username = data.get("username", None)
        if not participant_authentication_check(username):
            raise ValidationError("User: " + username + " does not exist")
        if not participant_login_check(username):
            raise ValidationError("User " + username + " is not logged in")
        return data


class AlertnessQuestionnairePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAlertnessRequest
        fields = '__all__'


class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = '__all__'


class LayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layout
        fields = '__all__'


class SetOccupancyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetOccupancyRequest
        fields = '__all__'


class DemographicQuestionnairePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostDemographicRequest
        fields = '__all__'


class ParticipantInWorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantWorkspace
        fields = '__all__'


class AlertnessTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlertnessTime
        fields = "__all__"


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAnalyticRequest
        fields = '__all__'


