from django.test import TestCase
from django.utils import timezone

from .models import *

"""
Developer instructions:
Run these tests using manage.py test
"""


# Partipant tests
class UserTest(TestCase):
    """
    Model tests
    """

    @staticmethod
    def create_user(username,
                    password):
        return User.objects.create(username=username,
                                   password=password)

    @staticmethod
    def create_participant(username,
                           survey_done,
                           in_workspace,
                           room,
                           desk,
                           profile):
        return Participant.objects.create(username=username,
                                          survey_done=survey_done,
                                          in_workspace=in_workspace,
                                          room=room,
                                          desk=desk,
                                          profile=profile)

    def create_default(self):
        return UserTest.create_user("test@test.com", "12345")

    def create_default_participant(self):
        return  UserTest.create_participant(UserTest.create_default(), False, False, 1, 1, 1)

    def test_participant_creation(self):
        participant = UserTest.create_participant()
        self.assertTrue(isinstance(participant, Participant))
        self.assertEqual(participant.__str__(), participant.username)


# Room tests
class RoomTest(TestCase):
    """
    Model tests
    """

    @staticmethod
    def create_room(name, x_length, y_length):
        return Room.objects.create(room_name=name, x_length=x_length, y_length=y_length)

    def create_default(self):
        return RoomTest.create_room("MFXXX", 555, 555)

    def test_room_creation(self):
        room = RoomTest.create_default()
        self.assertTrue(isinstance(room, Room))
        self.assertEqual(room.__str__(), room.room_name)


# Table tests
class DeskTest(TestCase):
    """
    Model tests
    """

    @staticmethod
    def create_table(room, number,
                     pos_x, pos_y, length_x, length_y, illuminance):
        return Desk.objects.create(room=room, number=number,
                                    pos_x=pos_x, pos_y=pos_y, length_x=length_x, length_y=length_y, illuminance=illuminance)

    def create_default(self):
        return DeskTest.create_table(RoomTest.create_default(), 1, 1, 1, 1, 1, 1)

    def test_table_creation(self):
        desk = DeskTest.create_default()
        self.assertTrue(isinstance(desk, Desk))
        self.assertEqual(desk.__str__(), "Table " + str(desk.number))


# Chair tests
class ChairTest(TestCase):
    """
    Model tests
    """

    @staticmethod
    def create_chair(desk, side, occupied):
        return Chair.objects.create(desk=desk, side=side, occupied=occupied)


    def create_default(self):
        return DeskTest.create_table(DeskTest.create_default(), 1, 1)


    def test_chair_creation(self):
        chair = ChairTest.create_default()
        self.assertTrue(isinstance(chair, Chair))
        self.assertEqual(chair.__str__(), "Chair " + str(chair.number))


# Sensor tests
class SensorTableTest(TestCase):
    """
    Model tests
    """

    @staticmethod
    def create_sensor(desk, date=timezone.now(), value=1000):
        return Sensor_Table.objects.create(desk=desk, date=date, value=value)

    def create_default(self):
        return SensorTableTest.create_sensor(DeskTest.create_default(), 1, 1)

    def test_sensor_creation(self):
        sensor = SensorTableTest.create_sensor()
        self.assertTrue(isinstance(sensor, Sensor_Table))
        self.assertEqual(sensor.__str__(), sensor.name)


# Sensor tests
class SensorUserTest(TestCase):
    """
    Model tests
    """

    @staticmethod
    def create_sensor(name="Test Sensor", date=timezone.now(), value=1000):
        return Sensor_Table.objects.create(name=name, date=date, value=value)

    def create_default(self):
        return SensorUserTest.create_sensor(DeskTest.create_default(), 1, 1)

    def test_sensor_creation(self):
        sensor = SensorTableTest.create_sensor()
        self.assertTrue(isinstance(sensor, Sensor_Table))
        self.assertEqual(sensor.__str__(), sensor.name)


# Window tests
class WindowTest(TestCase):
    """
    Model tests
    """

    @staticmethod
    def create_window(room=RoomTest.create_room(), start_pos=10, end_pos=20):
        return Window.objects.create(room=room, start_pos=start_pos, end_pos=end_pos)

    def test_window_creation(self):
        window = WindowTest.create_window()
        self.assertTrue(isinstance(window, Window))
        self.assertEqual(window.__str__(), "Window from " + str(window.start_pos) + " to " + str(window.end_pos))



