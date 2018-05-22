from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Model that defines the blueprint of a Room on the Database
class Room(models.Model):
    code = models.CharField(max_length=10)                              # code is a string of max length 10
    x_length = models.IntegerField()                                    # x_length is an integer of undefined length
    y_length = models.IntegerField()

    def get_absolute_url(self):
        return reverse('floorPlan:index')

    # Defines how a Room object is displayed
    def __str__(self):
        return self.code


# Model that defines the blueprint of a Table on the Database
class Table(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.IntegerField()
    x_pos = models.IntegerField()
    y_pos = models.IntegerField()
    x_size = models.IntegerField()
    y_size = models.IntegerField()

    def get_absolute_url(self):
        return reverse('floorPlan:index')

    # Defines how a Table object is displayed
    def __str__(self):
        return 'Table ' + str(self.number)


# Model that defines the blueprint of a Chair on the Database
class Chair(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    number = models.IntegerField()
    position = models.IntegerField()
    occupied = models.BooleanField(default=False)                        # occupied is a boolean, False when created

    def get_absolute_url(self):
        return reverse('floorPlan:index')

    # Defines how a Chair object is displayed
    def __str__(self):
        return 'Chair' + str(self.number)


# Model that defines the blueprint of a Sensor on the Database
class Sensor(models.Model):
    name = models.CharField(max_length=10)
    date = models.DateTimeField()
    value = models.FloatField()

    # Defines how a Sensor object is displayed
    def __str__(self):
        return self.name


# Model that defines the blueprint of a Window on the Database
class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_pos = models.IntegerField()
    end_pos = models.IntegerField()

    def get_absolute_url(self):
        return reverse('floorPlan:room_detail', kwargs={'pk': self.pk})

    # Defines how a Window object is displayed
    def __str__(self):
        return 'Window from '+str(self.start_pos) + ' to '+str(self.end_pos)


# Model that defines the blueprint of a Participant on the Database
class Participant(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    logged_in = models.BooleanField(default=False)
    survey_done = models.BooleanField(default=False)

    # Defines how a User object is displayed
    def __str__(self):
        return self.email







