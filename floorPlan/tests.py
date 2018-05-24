from django.test import TestCase
from django.utils import timezone

from .models import Room, Table, Chair, Sensor, Window, Participant

"""
Developer instructions:
Run these tests using manage.py test
"""

# Room tests
class RoomTest(TestCase):

	"""
	Model tests
	"""

	@staticmethod
	def create_room(code = "MF 7.82", x_length = 500, y_length = 500):
		return Room.objects.create(code = code, x_length = x_length, y_length = y_length)

	def test_room_creation(self):
		room = RoomTest.create_room()
		self.assertTrue(isinstance(room, Room))
		self.assertEqual(room.__str__(), room.code)

# Table tests
class TableTest(TestCase):

	"""
	Model tests
	"""

	@staticmethod
	def create_table(room = RoomTest.create_room(), 
		number = 1, x_pos = 10, y_pos = 10, x_size = 50, y_size = 50):
		return Table.objects.create(room = room, number = number, 
			x_pos = x_pos, y_pos = y_pos, x_size = x_size, y_size = y_size)

	def test_table_creation(self):
		table = TableTest.create_table()
		self.assertTrue(isinstance(table, Table))
		self.assertEqual(table.__str__(), "Table " + str(table.number))

# Chair tests
class ChairTest(TestCase):

	"""
	Model tests
	"""

	@staticmethod
	def create_chair(table = TableTest.create_table(),
		number = 1, position = 150, occupied = False):
		return Chair.objects.create(table = table, number = number, position = position, occupied = occupied)

	def test_chair_creation(self):
		chair = ChairTest.create_chair()
		self.assertTrue(isinstance(chair, Chair))
		self.assertEqual(chair.__str__(), "Chair " + str(chair.number))

# Sensor tests
class SensorTest(TestCase):

	"""
	Model tests
	"""

	@staticmethod
	def create_sensor(name = "Test Sensor", date = timezone.now(), value = 1000):
		return Sensor.objects.create(name = name, date = date, value = value)

	def test_sensor_creation(self):
		sensor = SensorTest.create_sensor()
		self.assertTrue(isinstance(sensor, Sensor))
		self.assertEqual(sensor.__str__(), sensor.name)

# Window tests
class WindowTest(TestCase):

	"""
	Model tests
	"""

	@staticmethod
	def create_window(room = RoomTest.create_room(), start_pos = 10, end_pos = 20):
		return Window.objects.create(room = room, start_pos = start_pos, end_pos = end_pos)

	def test_window_creation(self):
		window = WindowTest.create_window()
		self.assertTrue(isinstance(window, Window))
		self.assertEqual(window.__str__(), "Window from " + str(window.start_pos) + " to " + str(window.end_pos))

# Partipant tests < to be moved to its own app >
class ParticipantTest(TestCase):

	"""
	Model tests
	"""

	@staticmethod
	def create_participant(email = "test@test.com", password = "12345", logged_in = False, survey_done = False):
		return Participant.objects.create(email = email, password = password, logged_in = logged_in, survey_done = survey_done)

	def test_participant_creation(self):
		participant = ParticipantTest.create_participant()
		self.assertTrue(isinstance(participant, Participant))
		self.assertEqual(participant.__str__(), participant.email)
