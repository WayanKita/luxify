from django.db import models
from django.urls import reverse


class Room(models.Model):
    code = models.CharField(max_length=10)
    x_length = models.CharField(max_length=5)
    y_length = models.CharField(max_length=5)

    def get_absolute_url(self):
        return reverse('floorPlan:sandbox')

    def __str__(self):
        return self.code


class Table(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.CharField(max_length=5)
    x_pos = models.CharField(max_length=5)
    y_pos = models.CharField(max_length=5)
    x_size = models.CharField(max_length=5)
    y_size = models.CharField(max_length=5)

    def get_absolute_url(self):
        return reverse('floorPlan:sandbox')

    def __str__(self):
        return 'Table ' + self.number


class Chair(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    number = models.CharField(max_length=2)
    position = models.CharField(max_length=3)
    occupied = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('floorPlan:sandbox')

    def __str__(self):
        return 'Chair' + self.number


class Window(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_pos = models.CharField(max_length=3)
    end_pos = models.CharField(max_length=3)

    def get_absolute_url(self):
        return reverse('floorPlan:room_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Window from '+ self.start_pos + ' to '+ self.end_pos
