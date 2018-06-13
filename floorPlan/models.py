from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

# Models in Django represent skeleton (aka blueprints) for databases to create tables on the database
# Such table are initially empty and are populated through the program


# Model that defines the blueprint of a Room on the Database
from rest_framework.authtoken.models import Token


class Room(models.Model):
    room_name = models.CharField(max_length=10)                             # code is a string of max length 10
    x_length = models.IntegerField()                                        # x_length is an integer of undefined length
    y_length = models.IntegerField()

    def get_absolute_url(self):
        return reverse('floorPlan:room-plan')

    # Defines how a Room object is displayed
    def __str__(self):
        return self.room_name


# Model that defines the blueprint of a Table on the Database
class Desk(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="desk")
    number = models.IntegerField()                              # deskNumber
    pos_x = models.IntegerField()                               # posX
    pos_y = models.IntegerField()                               # posY
    length_x = models.IntegerField()                            # lengthX
    length_y = models.IntegerField()                            # lengthY
    illuminance = models.IntegerField()                         # illuminance
    # extra field chair on android app

    def get_absolute_url(self):
        return reverse('floorPlan:room-plan')

    # Defines how a Table object is displayed
    def __str__(self):
        return 'Desk ' + str(self.pk)

    # def __unicode__(self):
    #     return '%d: %s' % (self.number, self.illuminance)


# Model that defines the blueprint of a Chair on the Database
class Chair(models.Model):
    desk = models.OneToOneField(Desk, on_delete=models.CASCADE, related_name="chair")
    side = models.IntegerField()
    occupied = models.BooleanField(default=False)                        # occupied is a boolean, False when created

    def get_absolute_url(self):
        return reverse('floorPlan:room-plan')

    # Defines how a Chair object is displayed
    def __str__(self):
        return 'Chair ' + str(self.pk)


# Model that defines the blueprint of a Sensor on the Database
class Sensor_Table(models.Model):
    table = models.ForeignKey(Desk, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    light_value = models.FloatField()
    occupancy_value = models.FloatField()

    # Defines how a Sensor object is displayed
    def __str__(self):
        return str(self.table) + ': ' + str(self.light_value)


# Model that defines the blueprint of a Window on the Database  # android application names
class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="window")
    margin = models.IntegerField()                              # margin
    length = models.IntegerField()                              # length
    side = models.IntegerField()                                # side; int[1-4] defines the side the window is on
    # pk -> windowID

    def get_absolute_url(self):
        return reverse('floorPlan:room-plan')

    # Defines how a Window object is displayed
    def __str__(self):
        return 'Window from '+str(self.margin) + ' to '+str(self.length+self.margin)

    # def __unicode__(self):
    #     return '%d: %s' % (self.length, self.side)


# Model that defines the blueprint of a Window on the Database  # android application names
class Door(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="door")
    margin = models.IntegerField()                              # margin
    length = models.IntegerField()                              # length
    side = models.IntegerField()                                # side; int[1-4] defines the side the window is on
    # pk -> windowID

    def get_absolute_url(self):
        return reverse('floorPlan:room-plan')

    # Defines how a Window object is displayed
    def __str__(self):
        return 'Door from '+str(self.margin) + ' to '+str(self.length+self.margin)


# Model that defines the blueprint of a Participant on the Database     # Android naming
class Participant(models.Model):                                        # User object
    username = models.OneToOneField(User, on_delete=models.CASCADE)   # username                        # password
    survey_done = models.BooleanField(default=False)                    # demographicStatus ; not used
    in_workspace = models.BooleanField(default=False)                   # demographicStatus ; not used
    room = models.IntegerField(blank=True, null=True, default=1)        # roomID
    chair = models.IntegerField(blank=True, null=True, default=1)        # deskID
    profile = models.IntegerField(blank=True, null=True, default=1)        # deskID
    user_category = models.IntegerField(blank=True, null=True, default=0)

    # Defines how a User object is displayed
    def __str__(self):
        return str(self.username)


# Model that defines the blueprint of a Sensor on the Database
class Sensor_User(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    light_value = models.IntegerField()

    # Defines how a Sensor object is displayed
    def __str__(self):
        return str(self.participant)


# Model that defines format for alertness questionnaire answers storage
class AlertnessQuestionnaire(models.Model):
    username = models.ForeignKey(Participant, on_delete=models.CASCADE)
    answer = models.IntegerField()
    time_stamp = models.DateTimeField()

    def __str__(self):
        return str(self.username) + " answered: " + str(self.answer)


# Model that defines format for alertness questionnaire answers storage
class DemographicQuestionnaire(models.Model):
    username = models.ForeignKey(Participant, on_delete=models.CASCADE)
    answer = models.CharField(max_length=250)
    time_stamp = models.DateTimeField()

    def __str__(self):
        return str(self.username) + " answered: " + str(self.answer)


# Model that defines user profile based on answers given to questionnaire
class ParticipantProfiles(models.Model):
    answer = models.CharField(max_length=50)
    profile = models.IntegerField()

    def __str__(self):
        return str(self.answer)+" answer is profile : "+str(self.profile)

    class Meta:
        verbose_name_plural = "participant profiles"


# Model that defines format for analytics being sent by the mobile application
class Analytics(models.Model):
    username = models.ForeignKey(Participant, on_delete=models.CASCADE)
    # username = models.CharField(max_length=250)
    event = models.CharField(max_length=250)
    time_stamp = models.DateTimeField()

    def __str__(self):
        return str(self.event)+" recorded for : "+str(self.username)

    class Meta:
        verbose_name_plural = "analytics"


# WORK related models | DUMMY MODELS
# Used to simplify API testing
class ParticipantRequest(models.Model):
    username = models.CharField(max_length=200)
    request_type = models.IntegerField(blank=True)

    
# Used to simplify API testing
class UserRequest(models.Model):
    username = models.CharField(max_length=200)
    request_type = models.IntegerField(blank=True)


class ParticipantWorkspace(models.Model):
    username = models.CharField(max_length=200)
    in_workspace = models.BooleanField(default=False)
    room = models.IntegerField()


class ChairPostTest(models.Model):
    chair = models.IntegerField()


class PostDemographicRequest(models.Model):
    username = models.CharField(max_length=200)
    answer = models.CharField(max_length=250)
    time_stamp = models.DateTimeField()


class PostAlertnessRequest(models.Model):
    username = models.CharField(max_length=200)
    answer = models.IntegerField()
    time_stamp = models.DateTimeField()


class SetOccupancyRequest(models.Model):
    key = models.IntegerField()
    occupied = models.IntegerField()


class PostAnalyticRequest(models.Model):
    username = models.CharField(max_length=200)
    event = models.CharField(max_length=200)
    time_stamp = models.DateTimeField()


class UserCategory(models.Model):

    USER_CATEGORY = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
    )

    user_category = models.IntegerField(choices=USER_CATEGORY, unique=True)
    recommendation = models.BooleanField(default=False)
    visualization = models.BooleanField(default=False)
    guidance = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_category)+" : " + \
               str(self.recommendation)+", " + \
               str(self.visualization)+", " + \
               str(self.guidance)

    class Meta:
        verbose_name_plural = "user categories"

class Sensor(models.Model):
    column_number = models.IntegerField()
    sensor_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.sensor_name + ' (column ' + str(self.column_number) + ')'


class Layout(models.Model):
    LAYOUT = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
    )
    layout = models.IntegerField(choices=LAYOUT, unique=True)
    recommendation = models.BooleanField(default=False)
    visualization = models.BooleanField(default=False)
    guidance = models.BooleanField(default=False)

    def __str__(self):
        return "Layout "+str(self.layout)+" : " + \
               str(self.recommendation)+", " + \
               str(self.visualization)+", " + \
               str(self.guidance)

















