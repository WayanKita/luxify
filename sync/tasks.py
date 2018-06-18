import os, csv, sys, glob

from django.conf import settings
from celery import task
from floorPlan.models import Desk, SensorHistory, Sensor
from django.utils import timezone

path = settings.SYNC_PATH

@task
def task_number_one():
	if settings.SYNC_ENABLED:
		desks = Desk.objects.exclude(illuminance_sensor__isnull=True).exclude(occupancy_sensor__isnull=True)
		all_files = os.listdir(path)
		files = [fname for fname in all_files if fname.endswith('.csv')]
		# file = max(files, key = os.path.getmtime())
		glob_pattern = os.path.join(path, '*.csv')
		file = max(glob.iglob(glob_pattern), key=os.path.getctime)
		with open(file) as f:
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
						desk.illuminance = float(row[desk.illuminance_sensor.column_number])
						desk.occupied = int(row[desk.occupancy_sensor.column_number])
						desk.save()
						SensorHistory.objects.create(desk=desk, time_stamp=timezone.now(), light_value=float(row[illuminance_column]), occupancy_value=int(row[occupancy_column]))
				#os.rename(path + '/' + file, path + '/archives/' + file)
