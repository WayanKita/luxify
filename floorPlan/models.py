from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Room(models.Model):
    code = models.CharField(max_length=10)
    x_length = models.IntegerField()
    y_length = models.IntegerField()

    def get_absolute_url(self):
        return reverse('floorPlan:sandbox')

    def __str__(self):
        return self.code


class Table(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.IntegerField()
    x_pos = models.IntegerField()
    y_pos = models.IntegerField()
    x_size = models.IntegerField()
    y_size = models.IntegerField()

    def get_absolute_url(self):
        return reverse('floorPlan:sandbox')

    def __str__(self):
        return 'Table ' + str(self.number)


class Chair(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    number = models.IntegerField()
    position = models.IntegerField()
    occupied = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('floorPlan:sandbox')

    def __str__(self):
        return 'Chair' + str(self.number)


class Sensor(models.Model):
    name = models.CharField(max_length=5)
    date = models.DateTimeField()
    value = models.FloatField()


class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_pos = models.IntegerField()
    end_pos = models.IntegerField()

    def get_absolute_url(self):
        return reverse('floorPlan:room_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Window from '+str(self.start_pos) + ' to '+str(self.end_pos)


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=5)
    email_address = models.CharField(
        unique=True, max_length=250
    )

    def __str__(self):
        return str(self.user)


class Wayan(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    loggedIn = models.BooleanField(default=False)

    def __str__(self):
        return self.email







