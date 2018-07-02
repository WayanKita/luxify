from django.db import models


"""
Room models
"""


class Room(models.Model):

    """
    Represents a room in which experiments take place
    """

    name = models.CharField(max_length=250, unique=True)  # the name of the room

    def __str__(self):
        return self.name


class Side(models.Model):

    """
    An abstract class that represents one of four sides where an item can be placed
    """

    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4

    SIDES = (
        (TOP, 'Top'),
        (RIGHT, 'Right'),
        (BOTTOM, 'Bottom'),
        (LEFT, 'Left')
    )

    side = models.IntegerField(choices=SIDES)  # the side where the item is placed

    class Meta:
        abstract = True  # abstract class


class RoomItem(Side):

    """
    An abstract class that represents an item in the experiment room
    """

    margin = models.IntegerField()  # the margin from the room item side's corner as the origin
    length = models.IntegerField()  # the length of the room item

    class Meta:
        abstract = True  # abstract class


class Door(RoomItem):

    """
    Represents a door in the experiment room
    """

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='door')  # the room the door is in

    def __str__(self):
        return 'Door (' + str(self.pk) + ') in room ' + str(self.room)


class Window(RoomItem):

    """
    Represents a window in the experiment room
    """

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='window')  # the room the window is in

    def __str__(self):
        return 'Window (' + str(self.pk) + ') in room ' + str(self.room)


class Sensor(models.Model):

    """
    Represents a sensor
    """

    name = models.CharField(max_length=250, unique=True)  # the name of the sensor
    column = models.IntegerField()  # the column number of the sensor in the CSV file

    def __str__(self):
        return self.name + ' (column ' + str(self.column) + ')'


class Desk(Side):

    """
    Represents a desk in the experiment room
    """

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='desk')  # the room the desk is in
    illuminance_sensor = models.ForeignKey(
        Sensor, on_delete=models.SET_NULL,
        related_name='illuminance_sensor',
        blank=True, null=True)  # the illuminance sensor at the desk
    occupancy_sensor = models.ForeignKey(
        Sensor, on_delete=models.SET_NULL,
        related_name='occupancy_sensor',
        blank=True, null=True)  # the occupancy sensor at the desk
    side = models.IntegerField(
        choices=Side.SIDES,
        verbose_name='chair side')  # the side at which the chair is placed
    pos_x = models.IntegerField()  # the x-coordinate of the desk in pixels
    pos_y = models.IntegerField()  # the y-coordinate of the desk in pixels
    illuminance = models.FloatField(default=0)  # the illuminance value measured at the desk
    occupied = models.BooleanField(default=False)  # the occupancy of the desk
    score = models.FloatField(default=0)  # used to recommend a desk

    def __str__(self):
        return 'Desk (' + str(self.pk) + ') in room ' + str(self.room)

    def recommended_desks(room, target_illuminance):

        """
        Returns the desks ordered according to the target illuminance
        """

        desks_in_room = Desk.objects.filter(room=room)

        for desk in desks_in_room:
            if desk.occupied:
                desks_in_room = desks_in_room.exclude(pk=desk.pk)
            desk.score = abs(target_illuminance - desk.illuminance)
            desk.save()

        return desks_in_room.order_by('score')


class SensorLog(models.Model):

    """
    Represents the values measured by sensors at a point in time
    """

    desk = models.ForeignKey(
        Desk,
        on_delete=models.CASCADE,
        related_name='sensor_log')  # the desk at which the values were measured
    timestamp = models.DateTimeField()  # the time at which the values were measured
    illuminance = models.FloatField()  # the illuminance value at the desk
    occupied = models.BooleanField(default=False)  # the occupancy of the desk

    def __str__(self):
        return str(self.desk) + ': ' + str(self.illuminance) + ' at ' + self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
