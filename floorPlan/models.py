from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from rest_framework.authtoken.models import Token

# TODO: remove models linked with API serializers, complete SERIALIZERs todo before
# TODO: add comments


class Sensor(models.Model):
    column_number = models.IntegerField()
    sensor_name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.sensor_name + ' (column ' + str(self.column_number) + ')'


class Room(models.Model):
    room_name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.room_name


class Desk(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="desk")
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    length_x = models.IntegerField()
    length_y = models.IntegerField()
    chair_side = models.IntegerField()
    illuminance = models.FloatField(default=0)
    score = models.FloatField(default=0)
    occupied = models.IntegerField(default=0)
    illuminance_sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, related_name="illuminance_sensor", null=True, blank=True)
    occupancy_sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, related_name="occupancy_sensor", null=True, blank=True)

    def __str__(self):
        return 'Desk ' + str(self.pk)


class SensorHistory(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    light_value = models.FloatField()
    occupancy_value = models.IntegerField()

    class Meta:
        verbose_name_plural = 'sensor history'

    def __str__(self):
        return str(self.desk) + ': ' + str(self.light_value)


class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="window")
    margin = models.IntegerField()
    length = models.IntegerField()
    side = models.IntegerField(default=1)

    def __str__(self):
        return 'Window from '+str(self.margin) + ' to '+str(self.length+self.margin)


class Door(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="door")
    margin = models.IntegerField()
    length = models.IntegerField()
    side = models.IntegerField()

    def __str__(self):
        return 'Door from '+str(self.margin) + ' to '+str(self.length+self.margin)


class Participant(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    survey_done = models.BooleanField(default=False)
    in_workspace = models.BooleanField(default=False)
    room = models.IntegerField(blank=True, null=True, default=None)
    desk = models.IntegerField(blank=True, null=True, default=None)
    profile = models.IntegerField(blank=True, null=True, default=None)
    user_category = models.IntegerField(blank=True, null=True, default=0)
    name = models.CharField(max_length=50, blank=True, null=True, default=None)

    def __str__(self):
        return str(self.username)


class AlertnessQuestionnaire(models.Model):
    username = models.ForeignKey(Participant, on_delete=models.CASCADE)
    answer = models.IntegerField()
    time_stamp = models.DateTimeField()

    def __str__(self):
        return str(self.username) + " answered: " + str(self.answer)


class DemographicQuestionnaire(models.Model):
    username = models.ForeignKey(Participant, on_delete=models.CASCADE)
    answer = models.CharField(max_length=250)
    time_stamp = models.DateTimeField()

    def __str__(self):
        return str(self.username) + " answered: " + str(self.answer)


class ParticipantProfiles(models.Model):
    answer = models.CharField(max_length=50)
    profile = models.IntegerField()

    def __str__(self):
        return str(self.answer)+" answer is profile : "+str(self.profile)

    class Meta:
        verbose_name_plural = "participant profiles"


class Analytics(models.Model):
    username = models.ForeignKey(Participant, on_delete=models.CASCADE)

    event = models.CharField(max_length=250)
    time_stamp = models.DateTimeField()

    def __str__(self):
        return str(self.event)+" recorded for : "+str(self.username)

    class Meta:
        verbose_name_plural = "analytics"


class ParticipantRequest(models.Model):
    username = models.CharField(max_length=200)
    request_type = models.IntegerField(blank=True)


class UserRequest(models.Model):
    username = models.CharField(max_length=200)
    request_type = models.IntegerField(blank=True)


class ParticipantWorkspace(models.Model):
    username = models.CharField(max_length=200)
    in_workspace = models.BooleanField(default=False)
    room = models.IntegerField()


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


class Recommendation(models.Model):
    profile = models.OneToOneField(ParticipantProfiles, on_delete=models.CASCADE)
    formula = models.CharField(max_length=300, default="100000")

    def __str__(self):
        return str(self.profile.profile)+" has formula: "+str(self.formula)


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
               "Guidance: " + str(self.guidance)+", " + \
               "Recommendation: " + str(self.recommendation)+", " + \
               "Visualization: " + str(self.visualization)


class UserCategory(models.Model):
    user_category = models.ForeignKey(Layout, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'user categories'

    def __str__(self):
        return "User category "+self.user_category.pk+" has :"+str(self.user_category)


class AlertnessTime(models.Model):
    interval = models.IntegerField(verbose_name='interval (in minutes)')

    def __str__(self):
        return str(self.interval)