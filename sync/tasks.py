import os, csv, sys

from django.conf import settings
from celery import task
from floorPlan.models import Desk, Sensor_Table, Sensor
from .models import Date, SyncTest
from django.utils import timezone

path = settings.SYNC_PATH

@task
def task_number_one():
	if settings.SYNC_ENABLED:
		files = os.listdir(path)
		Date.objects.create()
		for file in files:
			if file.endswith('.csv'):
				with open (path + '/' + file) as f:
					reader = csv.reader(f)
					for row in reader:
						SyncTest.objects.create(row=row)
						if "Timestamp" in row:
							for idx, field in enumerate(row):
								if Sensor.objects.filter(sensor_name=field).exists():
									Sensor.objects.filter(sensor_name=field).update(column_number=idx)
								else:
									Sensor.objects.create(column_number=idx, sensor_name=field)
						if not "Timestamp" in row:
							pass
							# voltage_1 = row[4]
							# voltage_2 = row[5]
							# voltage_3 = row[6]
							# voltage_4 = row[7]
							# voltage_5 = row[8]
							# voltage_6 = row[9]
							# voltage_7 = row[10]
							# voltage_8 = row[11]
							# voltage_9 = row[12]
							# voltage_10 = row[13]
							# voltage_11 = row[14]
							# voltage_12 = row[15]
							# occ_1 = row[16]
							# occ_2 = row[17]
							# occ_3 = row[18]
							# occ_4 = row[19]
							# occ_5 = row[20]
							# occ_6 = row[21]

							# # UGLY HARDCODED
							# table_1 = Desk.objects.get(pk=1)
							# table_2 = Desk.objects.get(pk=2)
							# table_3 = Desk.objects.get(pk=3)
							# table_4 = Desk.objects.get(pk=4)
							# table_5 = Desk.objects.get(pk=5)
							# table_6 = Desk.objects.get(pk=6)

							# Sensor_Table.objects.create(table=table_1, time_stamp=timezone.now(), light_value=voltage_1, occupancy_value=occ_1)
							# Sensor_Table.objects.create(table=table_2, time_stamp=timezone.now(), light_value=voltage_2, occupancy_value=occ_2)
							# Sensor_Table.objects.create(table=table_3, time_stamp=timezone.now(), light_value=voltage_3, occupancy_value=occ_3)
							# Sensor_Table.objects.create(table=table_4, time_stamp=timezone.now(), light_value=voltage_4, occupancy_value=occ_4)
							# Sensor_Table.objects.create(table=table_5, time_stamp=timezone.now(), light_value=voltage_5, occupancy_value=occ_5)
							# Sensor_Table.objects.create(table=table_6, time_stamp=timezone.now(), light_value=voltage_6, occupancy_value=occ_6)
					os.rename(path + '/' + file, path + '/archives/' + file)
