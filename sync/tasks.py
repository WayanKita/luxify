import os, csv, sys

from django.conf import settings
from celery import task
from floorPlan.models import Desk, Sensor_History, Sensor
from django.utils import timezone

path = settings.SYNC_PATH

@task
def task_number_one():
	if settings.SYNC_ENABLED:
		desks = Desk.objects.exclude(illuminance_sensor__isnull=True).exclude(occupancy_sensor__isnull=True)
		files = os.listdir(path)
		for file in files:
			if file.endswith('.csv'):
				with open (path + '/' + file) as f:
					reader = csv.reader(f)
					for row in reader:
						if "Timestamp" in row:
							for idx, field in enumerate(row):
								if Sensor.objects.filter(sensor_name=field).exists():
									Sensor.objects.filter(sensor_name=field).update(column_number=idx)
								else:
									Sensor.objects.create(column_number=idx, sensor_name=field)
						if not "Timestamp" in row:
							for desk in desks:
								illuminance_column = desk.illuminance_sensor.column_number
								occupancy_column = desk.occupancy_sensor.column_number
								if row[illuminance_column].isdigit() and row[occupancy_column].isdigit():
									desk.illuminance = float(row[desk.illuminance_sensor.column_number])
									desk.occupied = int(row[desk.occupancy_sensor.column_number])
									desk.save()
									Sensor_History.objects.create(desk=desk, time_stamp=timezone.now(), light_value=illuminance_column, occupancy_value=occupancy_sensor)
					os.rename(path + '/' + file, path + '/archives/' + file)
