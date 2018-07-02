from django.test import TestCase
from django.utils import timezone
from app.models.room import Room, Door, Window, Sensor, Desk, SensorLog


"""
Room model tests
"""


class RoomTestCase(TestCase):

    """
    Room model tests
    """

    def setUp(self):
        self.room = Room.objects.create(name='Room')

    def test_field_name_name(self):
        """ test field name of name """
        field_label = self.room._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_max_length_name(self):
        """ test max length of name """
        max_length = self.room._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)

    def test_expected_output(self):
        """ test expected output when called as string """
        expected_output = self.room.name
        self.assertEquals(expected_output, str(self.room))


class DoorTestCase(TestCase):

    """
    Door model tests
    """

    def setUp(self):
        self.room = Room.objects.create(name='Room')
        self.door = Door.objects.create(room=self.room, margin=10, length=20, side=1)

    def test_field_name_room(self):
        """ test field name of room """
        field_label = self.door._meta.get_field('room').verbose_name
        self.assertEquals(field_label, 'room')

    def test_field_name_margin(self):
        """ test field name of margin """
        field_label = self.door._meta.get_field('margin').verbose_name
        self.assertEquals(field_label, 'margin')

    def test_field_name_length(self):
        """ test field name of length """
        field_label = self.door._meta.get_field('length').verbose_name
        self.assertEquals(field_label, 'length')

    def test_field_name_side(self):
        """ test field name of side """
        field_label = self.door._meta.get_field('side').verbose_name
        self.assertEquals(field_label, 'side')

    def test_expected_output(self):
        """ test expected output when called as string """
        expected_output = 'Door (' + str(self.door.pk) + ') in room ' + str(self.door.room)
        self.assertEquals(expected_output, str(self.door))


class WindowTestCase(TestCase):

    """
    Window model tests
    """

    def setUp(self):
        self.room = Room.objects.create(name='Room')
        self.window = Window.objects.create(room=self.room, margin=10, length=20, side=1)

    def test_field_name_margin(self):
        """ test field name of margin """
        field_label = self.window._meta.get_field('room').verbose_name
        self.assertEquals(field_label, 'room')

    def test_field_name_margin(self):
        """ test field name of margin """
        field_label = self.window._meta.get_field('margin').verbose_name
        self.assertEquals(field_label, 'margin')

    def test_field_name_length(self):
        """ test field name of length """
        field_label = self.window._meta.get_field('length').verbose_name
        self.assertEquals(field_label, 'length')

    def test_field_name_side(self):
        """ test field name of side """
        field_label = self.window._meta.get_field('side').verbose_name
        self.assertEquals(field_label, 'side')

    def test_expected_output(self):
        """ test expected output when called as string """
        expected_output = 'Window (' + str(self.window.pk) + ') in room ' + str(self.window.room)
        self.assertEquals(expected_output, str(self.window))


class SensorTestCase(TestCase):

    """
    Sensor model tests
    """

    def setUp(self):
        self.sensor = Sensor.objects.create(name='sensor', column=1)

    def test_field_name_name(self):
        """ test field name of name """
        field_label = self.sensor._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_field_name_column(self):
        """ test field name of column """
        field_label = self.sensor._meta.get_field('column').verbose_name
        self.assertEquals(field_label, 'column')

    def test_max_length_name(self):
        """ test max length of name """
        max_length = self.sensor._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)

    def test_expected_output(self):
        """ test expected output when called as string """
        expected_output = self.sensor.name + ' (column ' + str(self.sensor.column) + ')'
        self.assertEquals(expected_output, str(self.sensor))


class DeskTestCase(TestCase):

    """
    Desk model tests
    """

    def setUp(self):
        self.room = Room.objects.create(name='Room')
        self.sensor_1 = Sensor.objects.create(name='sensor 1', column=1)
        self.sensor_2 = Sensor.objects.create(name='sensor 2', column=2)
        self.desk = Desk.objects.create(
            room=self.room, 
            illuminance_sensor=self.sensor_1,
            occupancy_sensor=self.sensor_2,
            side=3, pos_x=0, pos_y=0
        )

    def test_field_name_room(self):
        """ test field name of room """
        field_label = self.desk._meta.get_field('room').verbose_name
        self.assertEquals(field_label, 'room')

    def test_field_name_illuminance_sensor(self):
        """ test field name of name """
        field_label = self.desk._meta.get_field('illuminance_sensor').verbose_name
        self.assertEquals(field_label, 'illuminance sensor')

    def test_field_name_occupancy_sensor(self):
        """ test field name of name """
        field_label = self.desk._meta.get_field('occupancy_sensor').verbose_name
        self.assertEquals(field_label, 'occupancy sensor')

    def test_field_name_side(self):
        """ test field name of side """
        field_label = self.desk._meta.get_field('side').verbose_name
        self.assertEquals(field_label, 'chair side')

    def test_field_name_pos_x(self):
        """ test field name of pos_x """
        field_label = self.desk._meta.get_field('pos_x').verbose_name
        self.assertEquals(field_label, 'pos x')

    def test_field_name_pos_y(self):
        """ test field name of pos_x """
        field_label = self.desk._meta.get_field('pos_y').verbose_name
        self.assertEquals(field_label, 'pos y')

    def test_field_name_illuminance(self):
        """ test field name of illuminance """
        field_label = self.desk._meta.get_field('illuminance').verbose_name
        self.assertEquals(field_label, 'illuminance')

    def test_field_name_occupied(self):
        """ test field name of occupied """
        field_label = self.desk._meta.get_field('occupied').verbose_name
        self.assertEquals(field_label, 'occupied')

    def test_field_name_score(self):
        """ test field name of score """
        field_label = self.desk._meta.get_field('score').verbose_name
        self.assertEquals(field_label, 'score')

    def test_expected_output(self):
        """ test expected output when called as string """
        expected_output = 'Desk (' + str(self.desk.pk) + ') in room ' + str(self.desk.room)
        self.assertEquals(expected_output, str(self.desk))


class SensorLogTestCase(TestCase):

    """
    Sensor log model tests
    """

    def setUp(self):
        self.room = Room.objects.create(name='Room')
        self.sensor_1 = Sensor.objects.create(name='sensor 1', column=1)
        self.sensor_2 = Sensor.objects.create(name='sensor 2', column=2)
        self.desk = Desk.objects.create(
            room=self.room,
            illuminance_sensor=self.sensor_1,
            occupancy_sensor=self.sensor_2,
            side=3, pos_x=0, pos_y=0
        )
        self.sensorlog = SensorLog.objects.create(
            desk=self.desk,
            timestamp=timezone.now(),
            illuminance=1500,
            occupied=False
        )

    def test_field_name_desk(self):
        """ test field name of desk """
        field_label = self.sensorlog._meta.get_field('desk').verbose_name
        self.assertEquals(field_label, 'desk')

    def test_field_name_timestamp(self):
        """ test field name of timestamp """
        field_label = self.sensorlog._meta.get_field('timestamp').verbose_name
        self.assertEquals(field_label, 'timestamp')

    def test_field_name_illuminance(self):
        """ test field name of illuminance """
        field_label = self.sensorlog._meta.get_field('illuminance').verbose_name
        self.assertEquals(field_label, 'illuminance')

    def test_field_name_occupied(self):
        """ test field name of occupied """
        field_label = self.sensorlog._meta.get_field('occupied').verbose_name
        self.assertEquals(field_label, 'occupied')

    def test_expected_output(self):
        """ test expected output when called as string """
        expected_output = str(self.sensorlog.desk) + \
            ': ' + str(self.sensorlog.illuminance) + \
            ' at ' + self.sensorlog.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        self.assertEquals(expected_output, str(self.sensorlog))
